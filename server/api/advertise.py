import uuid

from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource

from .eth_utils.contractInterface import SpaceContractInterface, ERC721ContractInterface, ERC1155ContractInterface
from .auth.authorization import AuthorizationObject
# Temp test import. To be replaced with queries to DB
from .eth_utils.contracts.contractAddresses import test_ad_space_nft_contract_address_GOERLI_DEPLOYED
from .eth_utils.contracts.abi.nftADSpaceABI import nft_ad_space_nft_abi
from .eth_utils.contracts.contractAddresses import test_ad_space_nft_contract_REV01_address_GOERLI_DEPLOYED
from .eth_utils.contracts.abi.nftADSpaceABI_REV01 import nft_ad_space_abi_rev01
##################################


# Class for advertisement space provider resources
class Advertise(Resource):
    def __init__(self, **credentials):
        self.space_provider_id = credentials.get('space_provider_id', uuid.uuid4())  # Temp default value
        self.auth_token = credentials.get('auth_token', uuid.uuid4())  # Temp default value


    # GET ad_media referenced by ad_id
    def get(self, space_provider_id, ad_space_id):

        # Call DB handler to get info
        # GET ad media based on db server return of ad media response
        # response will return the nft contract address and the
        #if self.auth_token is None:
        #    return abort(404, message="AUTHORIZATION FAILED... Please check if you are authorized. " \
        #                              "Contact james.lynch.uml@gmail.com for assistance...")
        # db call ad_space_id --> ad_id -->  RETURN contract_address
        # db
        print(f"ad_space_id: {ad_space_id}")

        space_contract_interface = SpaceContractInterface(
            contract_address=test_ad_space_nft_contract_REV01_address_GOERLI_DEPLOYED,
            abi=nft_ad_space_abi_rev01)

        nft_ad_info = space_contract_interface.call_function_get_nft_ad_info()
        ad_media_url = space_contract_interface.call_function_token_uri(0)

        print(f"nft_ad_info: {nft_ad_info}")
        print(f"space_token_uri: {ad_media_url}")

        return {'ad_media_url': ad_media_url}, 200

    # POST new ad media reference to space contract
    def post(self, ad_space_id, ad_id):
        request_json = request.get_json(force=True)
        print(f"request_json: {request_json}")
        contract_address = request_json['contract_address']
        contract_type = request_json['contract_type']
        token_id = int(request_json['token_id'])
        space_id = request_json['space_id']
        # call db methods/endpoints to store data ad_id --> contract_address

        space_contract_interface = SpaceContractInterface(
            contract_address=test_ad_space_nft_contract_REV01_address_GOERLI_DEPLOYED,
            abi=nft_ad_space_abi_rev01)

        contract_response = space_contract_interface.call_function_set_nft_ad_info(contract_address=contract_address,
                                                                                   reference_token_id=token_id)

        return {'contract_response': contract_response}, 200
