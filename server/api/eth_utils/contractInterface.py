import json
import datetime
import os
from web3 import Web3
from retrying import retry
from solcx import compile_files, compile_source, install_solc, set_solc_version, compile_solc

from .provider import w3_infura, chain_id
from .contracts.abi.nftADSpaceABI_REV01 import nft_ad_space_abi_rev01
from .contracts.abi.erc721ABI import erc721_abi
from .contracts.abi.erc1155ABI import erc_1155_abi
from .contracts.abi.dutchAuctionABI_REV01 import dutch_auction_abi_rev01

from .config.ethConfigVars import TEST_WALLET_ADDRESS, TEST_WALLET_PRIVATE_KEY

install_solc(version='latest')
#compile_solc(version='latest')

base_path = os.path.split(__file__)[0]


# General Space contract interface. abi will generally use ERC721
class SpaceContractInterface:

    def __init__(self, contract_address=None, abi=None):
        self.contract_address = contract_address
        self.abi = abi
        
        self.contract_source_path = os.path.join(base_path, "contracts/solidity/nftADSpace_REV01.sol")
        self.contract_name = ':NFTADSpace'
        self.nonce = w3_infura.eth.get_transaction_count(TEST_WALLET_ADDRESS)

        if contract_address is not None:
            if abi is None:
                self.contract = w3_infura.eth.contract(address=contract_address, abi=nft_ad_space_abi_rev01)
            else:
                self.contract = w3_infura.eth.contract(address=contract_address, abi=abi)

            self.contract_function_list = list(self.contract.functions.__dict__.keys())[4:]

    def get_contract_address(self):
        return self.contract_address

    def get_abi(self):
        return self.abi

    def list_functions(self):
        return self.contract_function_list

    def deploy_contract(self, constructor_args=None):
        #  compile source code
        if constructor_args is None:
            compiled_sol = compile_files(source_files=self.contract_source_path, output_values=['abi', 'bin'])
        else:
            token_name = constructor_args['token_name']
            token_symbol = constructor_args['token_symbol']

            with open(self.contract_source_path, 'r') as solidity_file:
                solidity_source = solidity_file.read()

            original_string = 'ERC721("NFT AD Space", "NFTAS")'
            replacement_string = f'ERC721("{token_name}", "{token_symbol}")'

            solidity_source = solidity_source.replace(original_string, replacement_string)

            import_remapped = os.path.dirname(self.contract_source_path) + '/'
            compiled_sol = compile_source(source=solidity_source, output_values=['abi', 'bin'],
                                          base_path=import_remapped)

        for key in compiled_sol.keys():
            if self.contract_name in key:
                contract_id = key
        contract_interface = compiled_sol[contract_id]
        compiled_bytecode = contract_interface['bin']
        compiled_abi = contract_interface['abi']
        self.abi = compiled_abi

        contract = w3_infura.eth.contract(abi=compiled_abi, bytecode=compiled_bytecode)
        self.contract = contract

        txn = {"from": TEST_WALLET_ADDRESS, "nonce": self.nonce}
        constructor = contract.constructor().buildTransaction(txn)

        signed_txn = w3_infura.eth.account.sign_transaction(constructor, private_key=TEST_WALLET_PRIVATE_KEY)
        send_txn = w3_infura.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_receipt = w3_infura.eth.wait_for_transaction_receipt(send_txn)
        txn_receipt_json = Web3.toJSON(txn_receipt)
        self.contract_address = txn_receipt['contractAddress']

        return txn_receipt_json

    def call_function_safe_mint(self, to_address, token_uri):
        to = to_address
        uri = token_uri

        self.nonce = w3_infura.eth.get_transaction_count(TEST_WALLET_ADDRESS)
        txn = {"from": TEST_WALLET_ADDRESS, "nonce": self.nonce}

        self.contract = w3_infura.eth.contract(address=self.contract_address, abi=self.abi)
        estimated_gas = self.contract.functions.safeMint(to, uri).estimateGas(txn)
        txn['gasPrice'] = w3_infura.toWei("20", "gwei")
        txn['gas'] = estimated_gas

        function_call = self.contract.functions.safeMint(to, uri).buildTransaction(txn)

        signed_txn = w3_infura.eth.account.sign_transaction(function_call, private_key=TEST_WALLET_PRIVATE_KEY)
        send_txn = w3_infura.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_receipt = w3_infura.eth.wait_for_transaction_receipt(send_txn)

        txn_receipt_json = Web3.toJSON(txn_receipt)
        return txn_receipt_json

    def call_function_set_nft_ad_info(self, contract_address, reference_token_id):
        _nftContractAddress = contract_address
        _referenceTokenId = reference_token_id

        self.nonce = w3_infura.eth.get_transaction_count(TEST_WALLET_ADDRESS)
        txn = {"from": TEST_WALLET_ADDRESS, "nonce": self.nonce}
        function_call = self.contract.functions.setNftAdInfo(_nftContractAddress, _referenceTokenId).buildTransaction(txn)

        signed_txn = w3_infura.eth.account.sign_transaction(function_call, private_key=TEST_WALLET_PRIVATE_KEY)
        send_txn = w3_infura.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_receipt = w3_infura.eth.wait_for_transaction_receipt(send_txn)

        txn_receipt_json = Web3.toJSON(txn_receipt)
        return txn_receipt_json

    def call_function_get_nft_ad_info(self):
        response = self.contract.functions.getNftAdInfo().call()
        return response

    def call_function_token_uri(self, token_id):
        # default token uri = 1 for testing 11/5/2022
        response = self.contract.functions.tokenURI(token_id).call()
        return response


# ERC721
class ERC721ContractInterface:
    def __init__(self, contract_address=None, abi=None, token_id=None):
        self.contract_address = contract_address
        self.abi = abi
        self.token_id = token_id
        self.contract_source_path = os.path.join(base_path, "contracts/solidity/nftADSpace_REV01.sol")
        self.nonce = w3_infura.eth.get_transaction_count(TEST_WALLET_ADDRESS)

        if contract_address is not None:
            if abi is None:
                self.contract = w3_infura.eth.contract(address=contract_address, abi=erc721_abi)
            else:
                self.contract = w3_infura.eth.contract(address=contract_address, abi=abi)

            self.contract_function_list = list(self.contract.functions.__dict__.keys())[4:]

    def get_contract_address(self):
        return self.contract_address

    def get_abi(self):
        return self.abi

    def list_functions(self):
        return self.contract_function_list

    def deploy_contract(self):
        #  compile source code
        compiled_sol = compile_files(source_files=self.contract_source_path, output_values=['abi', 'bin'])

        contract_id, contract_interface = compiled_sol.popitem()
        compiled_bytecode = contract_interface['bin']
        compiled_abi = contract_interface['abi']

        contract = w3_infura.eth.contract(abi=compiled_abi, bytecode=compiled_bytecode)
        txn = {"from": TEST_WALLET_ADDRESS, "nonce": self.nonce, }
        constructor = contract.constructor().buildTransaction(txn)

        signed_txn = w3_infura.eth.account.sign_transaction(constructor, private_key=TEST_WALLET_PRIVATE_KEY)
        send_txn = w3_infura.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_receipt = w3_infura.eth.wait_for_transaction_receipt(send_txn)
        txn_receipt_json = Web3.toJSON(txn_receipt)

        return txn_receipt_json

    def call_function_token_uri(self):
        response = self.contract.functions.tokenURI(self.token_id).call()
        return response


# ERC1155
class ERC1155ContractInterface:
    def __init__(self, contract_address=None, abi=None, token_id=None):
        self.contract_address = contract_address
        self.abi = abi
        self.token_id = token_id
        self.contract_source_path = os.path.join(base_path, "contracts/solidity/nftADSpace_REV01.sol")
        self.nonce = w3_infura.eth.get_transaction_count(TEST_WALLET_ADDRESS)

        if contract_address is not None:
            if abi is None:
                self.contract = w3_infura.eth.contract(address=contract_address, abi=erc_1155_abi)
            else:
                self.contract = w3_infura.eth.contract(address=contract_address, abi=abi)

            self.contract_function_list = list(self.contract.functions.__dict__.keys())[4:]

    def get_contract_address(self):
        return self.contract_address

    def get_abi(self):
        return self.abi

    def list_functions(self):
        return self.contract_function_list

    def deploy_contract(self):
        #  compile source code
        compiled_sol = compile_files(source_files=self.contract_source_path, output_values=['abi', 'bin'])

        contract_id, contract_interface = compiled_sol.popitem()
        compiled_bytecode = contract_interface['bin']
        compiled_abi = contract_interface['abi']

        contract = w3_infura.eth.contract(abi=compiled_abi, bytecode=compiled_bytecode)
        txn = {"from": TEST_WALLET_ADDRESS, "nonce": self.nonce, }
        constructor = contract.constructor().buildTransaction(txn)

        signed_txn = w3_infura.eth.account.sign_transaction(constructor, private_key=TEST_WALLET_PRIVATE_KEY)
        send_txn = w3_infura.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_receipt = w3_infura.eth.wait_for_transaction_receipt(send_txn)
        txn_receipt_json = Web3.toJSON(txn_receipt)

        return txn_receipt_json

    def call_function_token_uri(self):
        response = self.contract.functions.uri(self.token_id).call()
        return response


# Dutch auction contract interface
class DutchAuctionContractInterface:
    def __init__(self, contract_address=None, abi=None):
        self.contract_address = contract_address
        self.abi = abi
        self.contract_source_path = os.path.join(base_path, "contracts/solidity/DutchAuction_REV01.sol")
        self.contract_name = ':DutchAuction'
        self.nonce = w3_infura.eth.get_transaction_count(TEST_WALLET_ADDRESS)

        if contract_address is not None:
            if abi is None:
                self.contract = w3_infura.eth.contract(address=contract_address, abi=dutch_auction_abi_rev01)
            else:
                self.contract = w3_infura.eth.contract(address=contract_address, abi=abi)
            self.contract_function_list = list(self.contract.functions.__dict__.keys())[4:]

    def get_contract_address(self):
        return self.contract_address

    def get_abi(self):
        return self.abi

    def list_functions(self):
        return self.contract_function_list

    def deploy_contract(self, constructor_args=None):
        #  compile source code
        compiled_sol = compile_files(source_files=self.contract_source_path, output_values=['abi', 'bin'])

        for key in compiled_sol.keys():
            if self.contract_name in key:
                contract_id = key
        contract_interface = compiled_sol[contract_id]
        compiled_bytecode = contract_interface['bin']
        compiled_abi = contract_interface['abi']
        self.abi = compiled_abi

        contract = w3_infura.eth.contract(abi=compiled_abi, bytecode=compiled_bytecode)
        self.contract = contract
        txn = {"from": TEST_WALLET_ADDRESS, "nonce": self.nonce, }

        constructor = contract.constructor(**constructor_args).buildTransaction(txn)
        signed_txn = w3_infura.eth.account.sign_transaction(constructor, private_key=TEST_WALLET_PRIVATE_KEY)
        send_txn = w3_infura.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_receipt = w3_infura.eth.wait_for_transaction_receipt(send_txn)
        txn_receipt_json = Web3.toJSON(txn_receipt)
        self.contract_address = txn_receipt['contractAddress']

        return txn_receipt_json

    def get_info(self):
        if self.contract.address is None:
            self.contract = w3_infura.eth.contract(address=self.contract_address, abi=self.abi)

        starting_price = self.contract.functions.startingPrice().call()
        starting_price_ether = str(Web3.fromWei(starting_price, 'ether'))

        current_price = self.contract.functions.getPrice().call()
        current_price_ether = str(Web3.fromWei(current_price, 'ether'))

        discount_rate = self.contract.functions.discountRate().call()
        discount_rate_ether = str(Web3.fromWei(discount_rate, 'ether'))

        auction_start_time = self.contract.functions.startAt().call()
        dt_auction_start_time = datetime.datetime.fromtimestamp(auction_start_time).strftime('%m/%d/%Y, %H:%M:%S')
        auction_expire_time = self.contract.functions.expiresAt().call()
        dt_auction_expire_time = datetime.datetime.fromtimestamp(auction_expire_time).strftime('%m/%d/%Y, %H:%M:%S')

        auctioned_nft_address = self.contract.functions.nft().call()
        auctioned_nft_token_id = self.contract.functions.nftId().call()

        auction_seller_address = self.contract.functions.seller().call()

        info = {
            "price": {
                "starting_price": starting_price_ether,
                "current_price": current_price_ether,
                "discount_rate": discount_rate_ether
            },
            "auction_time": {
                "auction_start": dt_auction_start_time,
                "auction_expire": dt_auction_expire_time
            },
            "auction_item_info": {
                "auctioned_nft_address": auctioned_nft_address,
                "auctioned_nft_token_id": auctioned_nft_token_id,
                "auction_seller_address": auction_seller_address
            }
        }

        return info

    def buy(self):
        return


class ContractInterfaceRouter:
    def __init__(self, contract_address=None, contract_type=None, contract_standard=None):
        if contract_type == 'space':
            self.contract_interface_object = SpaceContractInterface(contract_address=contract_address)
        if contract_type == 'advertisement':
            if contract_standard == 'erc721':
                self.contract_interface_object = ERC721ContractInterface(contract_address=contract_address)
            if contract_standard == 'erc1155':
                self.contract_interface_object = ERC1155ContractInterface(contract_address=contract_address)
        if contract_type == 'space_auction' or contract_type == 'advertisement_auction':
            self.contract_interface_object = DutchAuctionContractInterface(contract_address=contract_address)

    @retry(stop_max_attempt_number=5, wait_fixed=1000)
    def get_info(self):
        info = self.contract_interface_object.get_info()
        return info

    @retry(stop_max_attempt_number=5, wait_fixed=1000)
    def deploy_contract(self, constructor_args=None):
        txn_receipt = self.contract_interface_object.deploy_contract(constructor_args=constructor_args)
        txn_receipt_dict = json.loads(txn_receipt)
        return txn_receipt_dict
