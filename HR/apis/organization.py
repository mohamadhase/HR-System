# external imports
from flask_restx import Namespace, Resource
from flask import abort, request
# internal imports
from HR import db
from HR.models.Organization import Organization
from HR.models.Team import Team
from HR.models.Authentication import Authentication

# create the namespace for the organization API
api = Namespace('Organization', description='Organization related API')


@api.route('/info')
class OrganizationInfo(Resource):
    @api.doc(description='Get inforamtion about the  Organization', security='apikey')
    @api.response(200, 'success request', Organization.Organization_info)
    @api.response(400, 'invalid arguments')
    @api.response(404, 'Organization not found')
    @api.param('teams', 'spicify if you want to get teams or not', type=int, default=0)
    @api.param('employees', 'spicify if you want to get employees or not', type=int, default=0)
    @api.response(401, 'Unauthorized')
    @Authentication.token_required
    def get(orgnization_ID, self):
        # get the arguments
        teams = request.args.get('teams')
        employees = request.args.get('employees')
        # check if the orgnization exists
        if not Organization.is_exists(orgnization_ID):
            abort(404, 'Organization not found')
        # validate the teams and employees arguments
        try:
            teams = int(teams)
            if teams not in [0, 1]:
                raise ValueError
        except ValueError:
            abort(400, f'Invalid argument teams -> {teams}')
        try:
            employees = int(employees)
            if employees not in [0, 1]:
                raise ValueError
        except ValueError as e:
            abort(400, f'Invalid argument employees -> {employees}')
        # get the organization information
        org_info = Organization.get_info(orgnization_ID, teams, employees)
        # delete the password from the returned object
        org_info.pop('Password')
        # return the organization information with success status
        return org_info, 200

    @api.doc(description='Update the Organization informations', security='apikey')
    @api.param('Name', 'New Organization Name')
    @api.param('Address', 'New Adress Description')
    @api.response(200, 'Organization updated', Organization.Organization_info)
    @api.response(404, 'Organization not found')
    @api.response(401, 'Unauthorized')
    @Authentication.token_required
    def patch(orgnization_ID, self):
        # check if the orgnization exists
        if not Organization.is_exists(orgnization_ID):
            abort(404, 'Organization Not Found')
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
        return org_info, 200
