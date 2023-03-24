import requests
import os
from dotenv import dotenv_values, find_dotenv

# TODO: Create a way to get config vars from .env file
config = dotenv_values(dotenv_path=find_dotenv())


class Creator:
    def __init__(self, db_endpoint=None, req_body=None):
        if db_endpoint is None:
            self.db_endpoint = config["DB_ENDPOINT"]
        else:
            self.db_endpoint = db_endpoint

        self.req_body = req_body

    def create_user(self):
        response = requests.post(self.db_endpoint + "/user", json=self.req_body)
        return response

    def create_contract(self):
        response = requests.post(self.db_endpoint + "/contract", json=self.req_body)
        return response

    def create_auction(self):
        response = requests.post(self.db_endpoint + "/auction", json=self.req_body)
        return response

    def create_space(self):
        response = requests.post(self.db_endpoint + "/space", json=self.req_body)
        return response

    def create_advertisement(self):
        response = requests.post(self.db_endpoint + "/advertisement", json=self.req_body)
        return response
