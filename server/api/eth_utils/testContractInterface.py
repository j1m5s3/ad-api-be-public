from contractInterface import SpaceContractInterface,ERC721ContractInterface,DutchAuctionContractInterface,ERC1155ContractInterface

from contracts.contractAddresses import test_ad_space_nft_contract_REV01_address_GOERLI_DEPLOYED
from contracts.abi.nftADSpaceABI_REV01 import nft_ad_space_abi_rev01

from contracts.contractAddresses import test_dutch_auction_contract_REV01_address_GOERLI_DEPLOYED
from contracts.abi.dutchAuctionABI_REV01 import ducth_auction_abi_rev01

space_contract_address = test_ad_space_nft_contract_REV01_address_GOERLI_DEPLOYED
space_contract_abi = nft_ad_space_abi_rev01

dutch_auction_address = test_dutch_auction_contract_REV01_address_GOERLI_DEPLOYED
dutch_auction_abi = ducth_auction_abi_rev01

if __name__ == "__main__":
    contract_interface = DutchAuctionContractInterface(contract_address=dutch_auction_address, abi=dutch_auction_abi)
    contract_functions = contract_interface.list_functions()
    print(contract_functions)
    auction_info = contract_interface.get_info()
    print(auction_info)
    pass
