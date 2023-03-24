from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource

from .eth_utils.contractInterface import SpaceContractInterface, ERC721ContractInterface, ERC1155ContractInterface
from .eth_utils.contracts.contractAddresses import test_ad_space_nft_contract_REV01_address_GOERLI_DEPLOYED
from .eth_utils.contracts.abi.nftADSpaceABI_REV01 import nft_ad_space_abi_rev01

# Class for Advertiser resources
class Advertiser(Resource):
    def __init__(self, ad_provider_id=None, ad_space_id=None, ad_id=None, auth_token=None):
        self.ad_provider_id = ad_provider_id
        self.ad_space_id = ad_space_id
        self.ad_id = ad_id
        self.auth_token = auth_token

    # GET ad_media referenced by ad_id
    def get(self, ad_provier_id):
        pass

    def post(self, ad_provider_id):
        # OWNED space_id
        # DB checks to verify if space_id is owned by ad_provider_id
        request_json = request.get_json(force=True)

        contract_address = request_json['contract_address']
        contract_type = request_json['contract_type']
        token_id = int(request_json['token_id'])
        space_id = request_json['space_id']

        space_contract_interface = SpaceContractInterface(
            contract_address=test_ad_space_nft_contract_REV01_address_GOERLI_DEPLOYED,
            abi=nft_ad_space_abi_rev01)

        contract_response = space_contract_interface.call_function_set_nft_ad_info(contract_address=contract_address,
                                                                                   reference_token_id=token_id)
        return {"contract_response": contract_response}, 200
