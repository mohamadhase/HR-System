# external imports
from flask_restx import Namespace, Resource
from flask import abort, request
from http import HTTPStatus 
import logging
# internal imports
from HR import db
from HR.models.Organization import Organization
from HR.models.Team import Team
from HR.models.Authentication import Authentication
from HR.models.Logger import *
import random
# create the namespace for the organization API
api = Namespace('Organization', description='Organization related API')
# create logger 
logger = create_logger(__name__)

@api.route('/info')
class OrganizationInfo(Resource):

    
    @api.doc(description='Get inforamtion about the  Organization', security='apikey')
    @api.response(HTTPStatus.OK.value, HTTPStatus.OK.phrase , Organization.Organization_info)
    @api.response(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.phrase)
    @api.response(HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.phrase)
    @api.response(HTTPStatus.UNAUTHORIZED.value, HTTPStatus.UNAUTHORIZED.phrase)
    @api.param('teams', 'spicify if you want to get teams or not', type=int, default=0)
    @api.param('employees', 'spicify if you want to get employees or not', type=int, default=0)
    @Authentication.token_required
    def get(orgnization_ID, self):
        logger.info('GET /organization/info')
        # get the arguments
        teams = request.args.get('teams')
        employees = request.args.get('employees')
        # check if the orgnization exists
        if not Organization.is_exists(orgnization_ID):
            logger.error(f'Organization not found Returning HTTP status code:{HTTPStatus.NOT_FOUND.value}')
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Organization not found'})
        # validate the teams and employees arguments
        try:
            teams = int(teams)
            if teams not in [0, 1]:
                raise ValueError
        except ValueError:
            logger.error(f'Invalid teams argument. teams = {teams},  Returning HTTP status code:{HTTPStatus.BAD_REQUEST.value}')
            abort(HTTPStatus.BAD_REQUEST.value, {'error':'teams argument must be 0 or 1'})
        try:
            employees = int(employees)
            if employees not in [0, 1]:
                raise ValueError
        except ValueError as e:
            logger.error(f'Invalid employees argument. employees = {employees},  Returning HTTP status code:{HTTPStatus.BAD_REQUEST.value}')
            abort(HTTPStatus.BAD_REQUEST.value, {'error':'employees argument must be 0 or 1'})
        # get the organization information
        org_info = Organization.get_info(orgnization_ID, teams, employees)
        # delete the password from the returned object
        org_info.pop('Password')
        # return the organization information with success status
        logger.info(f'Request completed successfully returning HTTP status code:{HTTPStatus.OK.value}')
        return org_info, HTTPStatus.OK.value


    @api.doc(description='Update the Organization informations', security='apikey')
    @api.param('Name', 'New Organization Name')
    @api.param('Address', 'New Adress Description')
    @api.response(HTTPStatus.OK.value, HTTPStatus.OK.phrase , Organization.Organization_info)
    @api.response(HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.phrase)
    @api.response(HTTPStatus.UNAUTHORIZED.value, HTTPStatus.UNAUTHORIZED.phrase)
    @Authentication.token_required
    def patch(orgnization_ID, self):
        logger.info('PATCH /organization/info')
        # check if the orgnization exists
        if not Organization.is_exists(orgnization_ID):
            logger.error(f'Organization not found Returning HTTP status code:{HTTPStatus.NOT_FOUND.value}')
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Organization not found'})
        # get current Organization info
        orgnization_info = Organization.get_info(orgnization_ID)
        # get the new Organization info
        if request.args.get("Name"):
            orgnization_info['Name'] = request.args.get("Name")

        if request.args.get("Address"):
            orgnization_info['Address'] = request.args.get("Address")
        # update the Organization info in the database
        
        org_info = Organization.update(orgnization_ID, orgnization_info)
        # delete the password from the returned object
        org_info.pop('Password')
        # return the organization information with success status
        logger.info(f'Request completed successfully returning HTTP status code:{HTTPStatus.OK.value}')
        return org_info, HTTPStatus.OK.value

    