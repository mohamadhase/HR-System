# external imports
from flask_restx import Namespace, Resource
from flask import abort, request

# internal imports
from HR import db
from HR.models.Organization import Organization
from HR.models.Team import Team
from HR.models.Authentication import Authentication

api = Namespace('Organization', description='Organization related API')


@api.route('/info')
class OrganizationInfo(Resource):
    @api.doc(description='Get inforamtion about the  Organization',security='apikey')
    @api.response(200, 'success request', Organization.Organization_info)
    @api.response(400, 'invalid arguments')
    @api.response(404, 'Organization not found')
    # add response for the teams and employees true and false
    @api.param('teams', 'spicify if you want to get teams or not', type=int, default=0)
    @api.param('employees', 'spicify if you want to get employees or not', type=int, default=0)
    @Authentication.token_required
    def get(orgnization_ID,self):
        teams = request.args.get('teams')
        employees = request.args.get('employees')

        # validate the orgnization_ID
        if not Organization.is_exists(orgnization_ID):
            abort(404, 'Organization not found')

        # validate the teams and employees parameters
        try:
            int(teams)
        except ValueError as e:
            abort(400, 'Invalid argument teams -> {teams}')
        try:
            int(employees)

        except ValueError as e:
            abort(400, 'Invalid argument employees -> {employees}')

        if int(teams) not in [0, 1]:
            abort(400, 'Invalid argument teams -> {teams}')
        if int(employees) not in [0, 1]:
            abort(400, 'Invalid argument employees -> {employees}')
        org_info = Organization.get_info(orgnization_ID,teams,employees)
        org_info.pop('Password')
        return org_info,200
         

    @api.doc(description='Update the Organization informations',security='apikey')
    @api.param('Name', 'New Organization Name')
    @api.param('Address', 'New Adress Description')
    @api.response(200, 'Organization updated', Organization.Organization_info)
    @api.response(404, 'Organization not found')
    @Authentication.token_required
    def patch(orgnization_ID,self):
        # validate the orgnization_ID
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
        return Organization.update(orgnization_ID, orgnization_info)
    


        
        

@api.route('/teams')
class OrganizationTeam(Resource):
    @api.doc(description='Get all teams in the Organization',security='apikey')
    @api.response(200, 'success request', [Team.team_info])
    @api.response(404, 'Organization not found')
    @Authentication.token_required
    def get(orgnization_ID,self):
        # validate the orgnization_ID
        if not Organization.is_exists(orgnization_ID):
            abort(404, 'Organization not found')
        return Organization.get_teams(orgnization_ID)
    
