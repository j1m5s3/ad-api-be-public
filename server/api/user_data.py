from flask import Flask, request, current_app, make_response
from flask_restful import Api, Resource
from flask_login import login_required, current_user
from datetime import datetime, timedelta

from .db_operations.getters import Getter


class UserData(Resource):

    @login_required
    def get(self):
        user_id = current_user.get_id()
        response = Getter().get_user_data(user_id=user_id)
        #print(response.json())
        return response.json()
    