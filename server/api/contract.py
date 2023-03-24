import uuid

from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource

from .eth_utils.contractInterface import ContractInterfaceRouter
from .eth_utils.contracts.contractAddresses import test_dutch_auction_contract_REV01_address_GOERLI_DEPLOYED


# Resource for handling contract calls, probably more specific to auction contract calls or contract creatiion
class Contract(Resource):

    #  TODO: Complete Contract operations switcher per contract_type 12/11/2022
    def post(self, contract_id):
        request_json = request.get_json(force=True)
        operation = request_json['operation']
        opertations = ["mint", "approve", "buy"]

    def get(self, contract_id):

        # Use contract_id to get info on contract such as...
        # contract_address and contract_abi
        # DB check here
        contract_id = contract_id
        contract_address = test_dutch_auction_contract_REV01_address_GOERLI_DEPLOYED
        #  Hard coded for testing 12/11/2022
        contract_type = "space_auction"
        contract_types = ["space", "advertisement", "space_auction", "advertisement_auction"]
        if contract_type in contract_types:
            contract_interface = ContractInterfaceRouter(contract_address=contract_address,
                                                         contract_type=contract_type)
        info = contract_interface.get_info()

        return info, 200

