# external imports
import datetime
from flask import abort,request
from flask_restx import fields
import hashlib
from functools import wraps
import jwt

# internal imports
from HR import db
from HR import api
from HR import app
from HR.models.Organization import Organization
class Authentication:
    register_orgnization = api.inherit('Register Organization', Organization.Organization_info, {
    'UserName': fields.String(required=True, description="Organization User Name"),
    'Password': fields.String(required=True, description="Organization Password")
    })
    login_orgnization = api.model('Login Organization', {
    'UserName': fields.String(required=True, description="Organization User Name"),
    'Password': fields.String(required=True, description="Organization Password")
    })
    @staticmethod
    def encrypt_password(password):
        # encrypt the password using sha256
        return hashlib.sha256(password.encode()).hexdigest()
    def register(org_info):
        db.collection('Organization').document(org_info['UserName']).set(org_info) 
        
    def token_required(f):
        @wraps(f)
        def decorated(*args,**kwargs):
            token = None
            if 'x-acess-token' in request.headers:
                token = request.headers['x-acess-token']
            if not token:
                abort(401, 'Token is missing')
            try :
                data =  jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                current_user = data['UserName']
            except :
                abort(401,'Token is invalid')
            return f(current_user,*args,**kwargs)
                
        return decorated
            