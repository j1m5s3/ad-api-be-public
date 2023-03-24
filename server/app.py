import json
import os
from flask import Flask, jsonify, request
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from dotenv import dotenv_values, find_dotenv

from api.advertise import Advertise
from api.advertiser import Advertiser
from api.contract import Contract
from api.deploy import DeployContract

from api.live_auction_list import LiveAuctionList
from api.create_auction import CreateAuction
from api.create_space import CreateSpace
from api.create_advertisement import CreateAdvertisement
from api.mint_space import MintSpace

from api.user_data import UserData

config = dotenv_values(dotenv_path=find_dotenv())

app = Flask(__name__)

with app.app_context():
    from api.login import Login
    from api.create_user import CreateUser

CORS(app, origins=['http://localhost:3000'])

app.config['SECRET_KEY'] = config['SECRET_KEY']
#app.config['SESSION_COOKIE_SECURE'] = True
#app.config['SESSION_COOKIE_HTTPONLY'] = True

api = Api(app)

#  TODO: Split routes described below to their own services
#  TODO: Remove the use of ids in the API routes and use the id stored in the flask.session 1/9/2023
api.add_resource(Advertise, '/advertise/<space_provider_id>')
api.add_resource(Advertiser, '/advertiser/<ad_provider_id>')
api.add_resource(Contract, '/contract/<contract_id>')
api.add_resource(DeployContract, '/deploy/<provider_id>')
api.add_resource(CreateUser, '/create_user')
api.add_resource(CreateSpace, '/create_space')
api.add_resource(LiveAuctionList, '/live_auctions')
api.add_resource(CreateAuction, '/create_auction')
api.add_resource(Login, '/login')
api.add_resource(UserData, '/user_data')
api.add_resource(CreateAdvertisement, '/create_advertisement')
api.add_resource (MintSpace, '/mint_space')


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
    pass
