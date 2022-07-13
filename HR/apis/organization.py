# external imports
import enum
from flask_restx import Namespace, Resource
from flask import abort, request

# internal imports
from HR import db
from HR.tools import Organization,Team

api = Namespace('Organization', description='Organization related API')

@api.route('/info')
class OrganizationInfo(Resource):
    @api.doc(description='Get inforamtion about the  Organization')
    @api.response(200, 'success request', Organization.Organization_info)
    @api.response(400, 'invalid arguments')
    @api.response(404, 'Organization not found')
    #add response for the teams and employees true and false
    
    @api.param('teams', 'spicify if you want to get teams or not', type=int, default=0)
    @api.param('employees', 'spicify if you want to get employees or not', type=int, default=0)

    def get(self):
        # get the org_id
        orgnization_ID = 'n0sy1NF8qUHyy46b1gI9'
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

        return Organization.get_Organization_info(
            orgnization_ID,
            teams,
            employees)

    @api.doc(description='Update the Organization informations')
    @api.param('Name', 'New Organization Name')
    @api.param('Address', 'New Adress Description')
    @api.response(200, 'Organization updated', Organization.Organization_info)
    @api.response(404, 'Organization not found')
    def patch(self):
        # get the org_id
        orgnization_ID = 'n0sy1NF8qUHyy46b1gI9'
        # validate the orgnization_ID
        if not Organization.is_exists(orgnization_ID):
            abort(404, 'Organization Not Found')
            
        #get current Organization info
        orgnization_info = Organization.get_info(orgnization_ID)

        # get the new Organization info
        if request.args.get("Name"):
            orgnization_info['Name'] = request.args.get("Name")
            
        if request.args.get("Address"):
            orgnization_info['Address'] = request.args.get("Address")
            
        # update the Organization info in the database
        return Organization.update(orgnization_ID,orgnization_info)

      


@api.route('/teams')
class OrganizationTeam(Resource):
    @api.doc(description='Get all teams in the Organization')
    @api.response(200, 'success request', [Team.team_info])
    @api.response(404, 'Organization not found')
    def get(self):
        # get the org_id
        orgnization_ID = 'n0sy1NF8qUHyy46b1gI9'
        # validate the orgnization_ID
        if not Organization.is_exists(orgnization_ID):
            abort(404, 'Organization not found')
        return Organization.get_teams(orgnization_ID)

    