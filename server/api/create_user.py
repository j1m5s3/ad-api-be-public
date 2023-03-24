from flask import Flask, request, current_app
from flask_login import LoginManager, login_user, logout_user
from flask_restful import reqparse, abort, Api, Resource
from flask_pydantic import validate

from .db_operations.models.models import User
from .db_operations.creators import Creator
from .db_operations.getters import Getter

app = current_app

# Initialize the LoginManager and set the user model
login_manager = LoginManager()
login_manager.init_app(app)


class CurrentUser:
    def __init__(self, user_id, user_name):
        self.user_id = user_id
        self.username = user_name
        self.is_active = True

    def get_id(self):
        return self.user_id


#@login_manager.user_loader
#def load_user(email_address):
#    # Replace this with a function that retrieves a user from the database
#    Getter.get_user_email_exists()
#    return User.get(email_address)


def login_view(email, password):
    # Replace this with a function that checks the username and password against the database
    response = Getter().get_user_by_email_and_password(email=email, password=password)
    data = response.json()
    if data['exists']:
        user_name = data['user_name']
        user_id = data['user_id']
        user = CurrentUser(user_id, user_name)
        if user:
            login_user(user)
            return True
    return False


def logout_view():
    logout_user()
    return
#  TODO: Update endpoint to handle user creation as well as logging in the new user


class CreateUser(Resource):

    @validate(body=User)
    def post(self):
        user_data = request.get_json(force=True)
        creator_response = Creator(db_endpoint=None, req_body=user_data).create_user()

        if creator_response.status_code == 400:
            return creator_response.json(), 400

        email_address = creator_response.json()['email_address']
        password = creator_response.json()['password']
        if login_view(email_address, password):
            return {"message": "User created and logged in successfully"}, 200