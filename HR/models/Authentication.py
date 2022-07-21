# external imports
import datetime
from flask import abort, request
from flask_restx import fields
import hashlib
from functools import wraps
import jwt
from http import HTTPStatus
# internal imports
from HR import db
from HR import api
from HR import app
from HR.models.Organization import Organization


class Authentication:
    register_orgnization = api.inherit('Register Organization', Organization.Organization_info, {
        'UserName': fields.String(required=True, description="Organization User Name"),
        'Password': fields.String(required=True, description="Organization Password"),
        
    })
    login_orgnization = api.model('Login Organization', {
        'UserName': fields.String(required=True, description="Organization User Name"),
        'Password': fields.String(required=True, description="Organization Password")
    })

    @staticmethod
    def encrypt_password(password: str) -> str:
        """encrypts the password using sha256 algorithm

        Args:
            password (str): password to be encrypted

        Returns:
            str: encrypted password in sha256 algorithm
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def register(org_info: dict) -> None:
        """ registers the Organization in the database

        Args:
            org_info (dict): Organization info to be registered
        """
        db.collection('Organization').document(
            org_info['UserName']).set(org_info)

    def token_required(f):
        """ decorator to check if the token is valid or not"""
        @wraps(f)
        def decorated(*args, **kwargs):
            """ decorator to check if the token is valid or not 

            Returns:
                function: returns the function if the token is valid with the user name 
            """
            token = None
            # get the token from the header if it is present
            if 'x-acess-token' in request.headers:
                token = request.headers['x-acess-token']
            # if no token is found, abort with 401 Unauthorized
            if not token:
                abort(HTTPStatus.UNAUTHORIZED, {'error': 'Token is missing'})
            try:
                # try to decode the token
                data = jwt.decode(
                    token, app.config['SECRET_KEY'], algorithms=['HS256'])
                # get the user name from the token if it is valid
                current_user = data['UserName']
            except:
                # if the token is invalid, abort with 401 Unauthorized
                abort(HTTPStatus.UNAUTHORIZED, {'error': 'Token is invalid'})
                # return the function with the current_user as parameter if the token is valid
            return f(current_user, *args, **kwargs)

        return decorated

    @staticmethod
    def generate_token(user_name: str) -> str:
        """ generates a token containing the user name and expiry time using sha256 algorithm

        Args:
            user_name (str): user name to be included in the token 

        Returns:
            str: token containing the user name and expiry time in sha256 algorithm
        """

        token = jwt.encode({'UserName': user_name, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return token
        
