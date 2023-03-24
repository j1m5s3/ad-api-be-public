import uuid
import json
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource

from .eth_utils.contractInterface import ContractInterfaceRouter


class DeployContract(Resource):

    def post(self, provider_id):

        request_json = request.get_json(force=True)
        contract_type = request_json['contract_type']
        contract_standard = None
        if 'contract_standard' in request_json.keys():
            contract_standard = request_json['contract_standard']
        contract_types = ["space", "advertisement"]
        if contract_type in contract_types:
            contract_interface = ContractInterfaceRouter(contract_address=None,
                                                         contract_type=contract_type,
                                                         contract_standard=contract_standard)
            response = contract_interface.deploy_contract()

            print("contractAddress: ", response['contractAddress'])
            return response, 200

        return {"Error": "Unable to deploy contract type {}".format(contract_type)}, 400


