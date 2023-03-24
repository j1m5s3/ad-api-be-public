from flask import request
from flask_restful import Resource
from flask_login import login_required, current_user

from .eth_utils.contractInterface import ContractInterfaceRouter

from .db_operations.creators import Creator
from .db_operations.getters import Getter


class MintSpace(Resource):

    @login_required
    def post(self):
        final_response = {}
        user_id = current_user.get_id()

        request_json = request.get_json(force=True)
        #contract_address = request_json['contract_address']
        contract_record_id  = request_json['ref_space_contract_id']
        contract_record = Getter().get_contract_by_id(contract_id=contract_record_id)
        if contract_record:
            contract_address = contract_record['contract_address']
            to_address = request_json['to_address']
            uri = request_json['uri']

            contract_interface = ContractInterfaceRouter(contract_address=contract_address,
                                                         contract_type="space",
                                                         contract_standard=None)
            mint_response = contract_interface.contract_interface_object.call_function_safe_mint(to_address=to_address,
                                                                                                 token_uri=uri)
            final_response['mint_response'] = mint_response

            db_create_space_record_request_body = {
                "is_space_ad_populated": False,
                "ref_space_contract_id": contract_record.json()['_id'],
                "space_provider_id": user_id
            }

            space_record = Creator(db_endpoint=None, req_body=db_create_space_record_request_body).create_space()
            final_response['space_record'] = space_record.json()

            final_response['message'] = "Space minted successfully"

            return final_response, 200
        else:
            return {"Error": "Unable to find contract record with id {}".format(contract_record_id)}, 400