import flask
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from flask_pydantic import validate

from .db_operations.getters import Getter
from .eth_utils.contractInterface import ContractInterfaceRouter


class LiveAuctionList(Resource):

    def get(self):
        auction_getter_response = Getter(db_endpoint=None).get_live_auctions()
        auction_getter_response_json = auction_getter_response.json()
        contract_info_list = self._get_data_from_db(auction_getter_response_json=auction_getter_response_json)

        return {"message": "Live auctions retrieved successfully", "data": contract_info_list}, 200

    @staticmethod
    def _get_data_from_db(auction_getter_response_json):

        contract_info_list = []
        for auction in auction_getter_response_json:
            contract_id = auction['ref_auction_contract_id']

            contract_getter_response = Getter(db_endpoint=None).get_contract_by_id(contract_id)
            contract_getter_response_json = contract_getter_response.json()

            contract_address = contract_getter_response_json['contract_address']
            contract_type = contract_getter_response_json['contract_type']
            contract_info = ContractInterfaceRouter(contract_address=contract_address,
                                                    contract_type=contract_type,
                                                    contract_standard=None).get_info()

            contract_info_list.append({"auction_record": auction,
                                       "contract_record": contract_getter_response_json,
                                       "on_chain_info": contract_info})
        return contract_info_list

