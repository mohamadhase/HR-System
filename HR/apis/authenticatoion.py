from flask_restx import Namespace, Resource
from flask import abort
from HR import app
import datetime
import jwt
# internal imports
from HR import api
from HR.models.Organization import Organization
from HR.models.Authentication import Authentication

api = Namespace('Authenticatoion', description='Authenticatoion related APIs')
@api.route('/login')
class LogIn(Resource):
    @api.doc('Login')
    @api.expect(Authentication.login_orgnization, validate=True)
    @api.response(200, 'Success')
    @api.response(401, 'Unauthorized')
    def post(self):
        #get the cridintials from the request
        cridintials = api.payload
        #encrypt the password
        cridintials['Password'] = Authentication.encrypt_password(cridintials['Password'])
        #check if the user exists
        if not  Organization.is_exists(cridintials['UserName']):
            abort(401, 'Login Failed')
        #get Organization from the database
        org_info = Organization.get_info(cridintials['UserName'])
        if org_info['Password'] != cridintials['Password']:
            abort(401, 'Login Failed')
        #create a token for the user
        token =  Authentication.generate_token(org_info['UserName']), 200
        #return the token
        return token
        

@api.route('/register')
class Register(Resource):
    @api.doc(description='Register')
    @api.expect(Authentication.register_orgnization,validate=True)
    @api.response(204, 'Organization registered')
    @api.response(409, 'Organization already exists')
    @api.response(400, 'Invalid arguments')
    def post(self):
        #get the new Organization info
        org_info  = api.payload
        #check user_name
        if org_info['UserName']=='':
            abort(400, 'Organization name is required')
        #check if the Organization already exists
        if Organization.is_exists(org_info['UserName']):
            abort(409, 'Organization with same username already exists')
        #encrypt the password
        org_info['Password'] = Authentication.encrypt_password(org_info['Password'])
        #register the Organization
        Authentication.register(org_info)
        return {'message': 'Organization registered'}, 201
    




        