from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from flask_pydantic import validate
from flask_login import login_required, current_user

from .db_operations.models.models import User
from .db_operations.creators import Creator
from .eth_utils.contractInterface import ContractInterfaceRouter


class CreateAuction(Resource):

    @login_required
    def post(self):
        """
        1. Deploy auction contract
        2. Start auction
        3. Create contract record in DB
        4. Create auction record in DB
        5. Return record data
        :return:
        """
        final_response = {}
        auction_data = request.get_json(force=True)
        print(auction_data)
        provider_id = current_user.get_id()

        contract_type = auction_data['contract_type']
        contract_constructor_args = auction_data['contract_constructor_args']

        contract_types = ["space_auction", "advertisement_auction"]
        if contract_type in contract_types:
            contract_interface = ContractInterfaceRouter(contract_address=None,
                                                         contract_type=contract_type,
                                                         contract_standard=None)
            deploy_response = contract_interface.deploy_contract(constructor_args=contract_constructor_args)
            final_response['deploy_response'] = deploy_response

            contract_address = deploy_response['contractAddress']
            db_create_contract_record_request_body = {
                "contract_address": contract_address,
                "contract_type": contract_type,
            }
            db_contract_response = Creator(db_endpoint=None,
                                           req_body=db_create_contract_record_request_body).create_contract()
            final_response['contract_record'] = db_contract_response.json()

            created_auction_info = contract_interface.get_info()
            print("created_auction_info: ", created_auction_info)
            end_date = created_auction_info['auction_time']['auction_expire']

            db_create_auction_record_request_body = {
                "is_complete": False,
                "ref_auction_contract_id": db_contract_response.json()['_id'],
                "ref_data": contract_constructor_args,
                "ref_provider_id": provider_id,
                "ref_space_contract_address": contract_constructor_args['_nft'],
                "ref_space_token_id": contract_constructor_args['_nftId'],
                "auction_end_date": end_date
            }
            db_auction_response = Creator(db_endpoint=None,
                                          req_body=db_create_auction_record_request_body).create_auction()
            final_response['auction_record'] = db_auction_response.json()

            return final_response, 200

            #db_response = Creator(db_endpoint=None, req_body=contract_info).create_contract()
        return {"Error": "Unable to deploy contract type {}".format(contract_type)}, 400
