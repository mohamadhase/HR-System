from flask_restx import  Namespace, Resource
from flask import request
from HR.models import organization_model
from HR import db

api = Namespace('Organization', description='Organization related API')

@api.route('/info')
class OrganizationInfo(Resource):
    @api.doc(description='Get  inforamtion about the  Organization')
    @api.response(200, 'Information about the Organization')
    def get(self):
        orgnization_ID = 'n0sy1NF8qUHyy46b1gI9'
        org_ref = db.collection('organization').document(orgnization_ID)
        orgnization_info =  org_ref.get().to_dict()
        orgnization_teams_ref = org_ref.collection('Teams').stream()
        orgnization_teams = []
        for team in orgnization_teams_ref:
            orgnization_teams.append(team.to_dict())
        orgnization_info['Teams'] = orgnization_teams

        orgnization_employees_ref = org_ref.collection('Employees').stream()
        orgnization_employees = []
        for employee in orgnization_employees_ref:
            orgnization_employees.append(employee.to_dict())
        orgnization_info['Employees'] = orgnization_employees
        
        return orgnization_info

    @api.doc(description='Update the Organization')
    @api.param('Name', 'New Organization Name')
    @api.param('Address', 'New Adress Description')

    def put(self):
        orgnization_ID = 'n0sy1NF8qUHyy46b1gI9'
        org_ref = db.collection('organization').document(orgnization_ID)
        orgnization_info = org_ref.get().to_dict()
        if request.args.get("Name"):
            orgnization_info['Name'] = request.args.get("Name")
        if request.args.get("Address"):
            orgnization_info['Address'] = request.args.get("Address")
        org_ref.update(orgnization_info)

        return orgnization_info

@api.route('/teams')
class OrganizationTeam(Resource):
    @api.doc(description='Get all teams in the Organization')
    def get(self):
        orgnization_ID = 'n0sy1NF8qUHyy46b1gI9'
        teams_ref = db.collection('organization').document(orgnization_ID).collection('Teams').stream()
        teams = []
        for team in teams_ref:
            teams.append(team.to_dict())
        return teams, 200            
     