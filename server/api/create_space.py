import uuid
import json
from flask import request
from flask_restful import Resource
from flask_login import login_required, current_user

from .eth_utils.contractInterface import ContractInterfaceRouter

from .db_operations.creators import Creator
from .db_operations.getters import Getter


class CreateSpace(Resource):

    @login_required
    def post(self):
        final_response = {}
        user_id = current_user.get_id()

        request_json = request.get_json(force=True)
        token_name = request_json['token_name']
        token_symbol = request_json['token_symbol']
        mint = request_json['mint']

        contract_interface = ContractInterfaceRouter(contract_address=None,
                                                     contract_type="space",
                                                     contract_standard=None)
        constructor_args = {'token_name': token_name, 'token_symbol': token_symbol}
        deploy_response = contract_interface.deploy_contract(constructor_args=constructor_args)
        final_response['deploy_response'] = deploy_response
        if mint:
            to_address = request_json['to_address']
            uri = request_json['uri']
            mint_response = contract_interface.contract_interface_object.call_function_safe_mint(to_address=to_address,
                                                                                          token_uri=uri)
            print("mint_response: ", mint_response)
            final_response['mint_response'] = mint_response

        contract_address = deploy_response['contractAddress']
        #  TODO: Add minted token_id to db record 1/15/2023
        db_create_contract_record_request_body = {
            "contract_address": contract_address,
            "contract_type": "space"
        }
        contract_record = Creator(db_endpoint=None,
                                  req_body=db_create_contract_record_request_body).create_contract()
        final_response['contract_record'] = contract_record.json()

        db_create_space_record_request_body = {
            "is_space_ad_populated": False,
            "ref_space_contract_id": contract_record.json()['_id'],
            "space_provider_id": user_id
        }
        space_record = Creator(db_endpoint=None, req_body=db_create_space_record_request_body).create_space()
        final_response['space_record'] = space_record.json()

        final_response['message'] = "Space created successfully"

        return final_response, 200

        #return {"Error": "Unable to deploy contract type {}".format(contract_type)}, 400



