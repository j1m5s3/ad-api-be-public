import jwt

from flask import Flask, request, current_app, make_response
from flask_restful import Api, Resource
from flask_login import LoginManager, login_user, logout_user, current_user

from datetime import datetime, timedelta

#from .db_operations.models.models import User
from .db_operations.getters import Getter

app = current_app

# Initialize the LoginManager and set the user model
login_manager = LoginManager()
login_manager.init_app(app)

# TEST
secret = 'secret'

# Login required paths
login_required_paths = ['/user_data', '/create_space', '/create_auction', '/create_advertisement']


class User:
    def __init__(self, user_id, user_name, is_authenticated, is_active=True):
        self.user_id = user_id
        self.username = user_name
        self.is_authenticated = is_authenticated
        self.is_active = is_active

    def get_id(self):
        return self.user_id

    def is_authenticated(self):
        return self.is_authenticated

    def is_active(self):
        return self.is_active


@login_manager.user_loader
def load_user(jwt_auth):
    decoded_user = jwt.decode(jwt_auth,
                              secret,
                              algorithms=['HS256'],
                              options={'verify_exp': True})

    user = Getter().get_user(user_id=decoded_user['user_id'])
    user_json = user.json()
    return User(user_id=user_json['_id'], user_name=user_json['user_name'], is_authenticated=True)


def login_view(email, password):
    # Replace this with a function that checks the username and password against the database
    response = Getter().get_user_by_email_and_password(email=email, password=password)
    data = response.json()
    if data['exists']:
        user_name = data['user_name']
        user_id = data['user_id']
        user = User(user_id, user_name, is_authenticated=True)
        if user:
            login_user(user)
            return {"logged_in": True, "user_id": user_id, "user_name": user_name}
    return {"logged_in": False}


def logout_view():
    logout_user()
    return


@app.before_request
def before_request():
    print("PATH: ", request.path)
    if request.path in login_required_paths:
        print(request.method)
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add("Access-Control-Allow-Headers", "Authorization, Content-Type")
            response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
            response.headers.add("Access-Control-Max-Age", "3600")
            return response
        print("PATH IN LOGIN REQUIRED PATHS")
        print("HEADERS: ", request.headers)
        if not request.headers.get('Authorization'):
            print("NO AUTH HEADER")
            return make_response({"logged_in": False}, 401)
        else:
            print("AUTH HEADER EXISTS")
            try:
                user = load_user(request.headers.get('Authorization'))
                if not user.is_authenticated:
                    print("USER NOT AUTHENTICATED")
                    return make_response({"message": "USER NOT AUTHENTICATED"}, 401)
            except jwt.ExpiredSignatureError:
                print("EXPIRED SIGNATURE")
                return make_response({"message": "EXPIRED SIGNATURE"}, 401)
            except jwt.InvalidTokenError:
                print("INVALID TOKEN")
                return make_response({"message": "INVALID TOKEN"}, 401)
            except Exception as e:
                print("EXCEPTION: ", e)
                return make_response({"message": e}, 401)
        login_user(user, remember=True)
        return
    return


class Login(Resource):

    def post(self):
        # Get the username and password from the request
        data = request.get_json()
        email_address = data['email_address']
        password = data['password']

        logged_in = login_view(email_address, password)
        if logged_in['logged_in']:
            # Step 3:
            # Generate a JWT
            payload = {
                'user_id': logged_in['user_id'],
                'username': logged_in['user_name'],
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }
            token = jwt.encode(payload, secret, algorithm='HS256')

            # Step 4:
            # Send the JWT to the client
            return {'message': 'Successfully logged in', 'token': token}, 200
        else:
            return {'message': 'Invalid email or password'}, 401

    @staticmethod
    def delete():
        logout_view()
        return {'message': 'Successfully logged out'}