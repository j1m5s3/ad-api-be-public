import requests
import os
from dotenv import dotenv_values, find_dotenv

# TODO: Create a way to get config vars from .env file
config = dotenv_values(dotenv_path=find_dotenv())


class Getter:
    def __init__(self, db_endpoint=None):
        if db_endpoint is None:
            self.db_endpoint = config["DB_ENDPOINT"]
        else:
            self.db_endpoint = db_endpoint

    def get_user(self, user_id):
        response = requests.get(self.db_endpoint + "/user/" + user_id)
        return response

    def get_user_data(self, user_id):
        response = requests.get(self.db_endpoint + "/user_data/" + user_id)
        return response

    def get_user_by_email_and_password(self, email, password):
        response = requests.get(self.db_endpoint + "/user/" + email + "/" + password)
        return response

    def get_user_email_exists(self, email):
        response = requests.get(self.db_endpoint + "/user/" + email + "/exists")
        return response

    def get_users(self):
        response = requests.get(self.db_endpoint + "/users")
        return response

    def get_space(self, space_id):
        response = requests.get(self.db_endpoint + "/space" + space_id)
        return response

    def get_spaces(self):
        response = requests.get(self.db_endpoint + "/spaces")
        return response

    def get_advertisement(self, advertisement_id):
        response = requests.get(self.db_endpoint + "/advertisement" + advertisement_id)
        return response

    def get_advertisements(self):
        response = requests.get(self.db_endpoint + "/advertisements")
        return response

    def get_auction(self, auction_id):
        response = requests.get(self.db_endpoint + "/auction" + auction_id)
        return response

    def get_live_auctions(self):
        response = requests.get(self.db_endpoint + "/live_auctions")
        return response

    def get_contract_by_id(self, contract_id):
        response = requests.get(self.db_endpoint + "/contract/" + contract_id)
        return response
