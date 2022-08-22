import random 
from time import sleep
from flask_restx import Namespace, Resource
from flask import abort
from http import HTTPStatus 


# internal imports
from HR import api,db
from HR.models.Organization import Organization
from HR.models.Authentication import Authentication
from HR.models.Logger import create_logger
from HR import celery

@celery.task(name='celery_exmaple.write_to_file')
def write_to_file(string):
    sleep(1)
    with open('demofile.txt','a') as f:
        f.write(f"{string}\n")
    return 'hi'


logger = create_logger(__name__)
api = Namespace('Authenticatoion', description='Authenticatoion related APIs')
@api.route('/login')
class LogIn(Resource):
    @api.doc('Login')
    @api.expect(Authentication.login_orgnization, validate=True)
    @api.response(HTTPStatus.OK.value, HTTPStatus.OK.phrase)
    @api.response(HTTPStatus.UNAUTHORIZED.value, HTTPStatus.UNAUTHORIZED.phrase)
    def post(self):
        logger.info("POST /login")
        
        #get the cridintials from the request
        cridintials = api.payload
        #encrypt the password
        cridintials['Password'] = Authentication.encrypt_password(cridintials['Password'])
        #check if the user exists
        if not  Organization.is_exists(cridintials['UserName']):
            logger.error(f"User {cridintials['UserName']} not found returning status code {HTTPStatus.UNAUTHORIZED.value}")
            abort(HTTPStatus.UNAUTHORIZED.value, {'error':'User not found'})
        #get Organization from the database
        org_info = Organization.get_info(cridintials['UserName'])
        if org_info['Password'] != cridintials['Password']:
            logger.error(f"Password mismatch returning status code {HTTPStatus.UNAUTHORIZED.value}")
            abort(HTTPStatus.UNAUTHORIZED.value, {'error':'Password is incorrect'})
        #create a token for the user
        token =  Authentication.generate_token(org_info['UserName']), HTTPStatus.OK.value
        #return the token
        logger.info(f"request completed returning status code {HTTPStatus.OK.value}")
        return token
        

@api.route('/register')
class Register(Resource):
    @api.doc(description='Register')
    @api.expect(Authentication.register_orgnization,validate=True)
    @api.response(HTTPStatus.CREATED.value, HTTPStatus.CREATED.phrase)
    @api.response(HTTPStatus.CONFLICT.value, HTTPStatus.CONFLICT.phrase)
    @api.response(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.phrase)
    def post(self):
        logger.info("POST /register")
        #get the new Organization info
        org_info  = api.payload
        #check user_name
        if org_info['UserName']=='':
            logger.error(f"User name is empty returning status code {HTTPStatus.BAD_REQUEST.value}")
            abort(HTTPStatus.BAD_REQUEST.value, {'error':'UserName is required'})
        #check if the Organization already exists
        if Organization.is_exists(org_info['UserName']):
            logger.error(f"Organization {org_info['UserName']} already exists returning status code {HTTPStatus.CONFLICT.value}")
            abort(HTTPStatus.CONFLICT.value, {'error':'UserName already exists'})
        #encrypt the password
        org_info['Password'] = Authentication.encrypt_password(org_info['Password'])
        #register the Organization
        Authentication.register(org_info)
        logger.info(f"request completed returning status code {HTTPStatus.CREATED.value}")
        return {'message': 'Organization registered'}, HTTPStatus.CREATED.value
    
    def get(self):

        write_to_file.delay('a')

@api.route('/register2')
class Reg(Resource):
    def get(self):
        write_to_file('b')
    
        

