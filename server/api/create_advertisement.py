from flask import request
from flask_restful import Resource
from flask_login import login_required, current_user

from .eth_utils.contractInterface import ContractInterfaceRouter

from .db_operations.creators import Creator


class CreateAdvertisement(Resource):

    @login_required
    def post(self):
        provider_id = current_user.get_id()

        #  TODO: Add validation for request body 1/22/2023
        request_json = request.get_json(force=True)

        media_reference = request_json['media_reference']
        description = request_json['description']

        creator_req_body = {"advertisement_provider_id": provider_id,
                            "media_reference": media_reference,
                            "description": description}

        creator_response = Creator(db_endpoint=None, req_body=creator_req_body).create_advertisement()

        return {"message": "Created Advertisement", "data": creator_response.json()}, 200