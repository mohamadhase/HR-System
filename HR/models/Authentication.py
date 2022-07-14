# external imports
import datetime
from flask import abort
from flask_restx import fields
import hashlib
# internal imports
from HR import db
from HR import api
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