from email.policy import strict
from warnings import catch_warnings
from flask_restx import  Namespace, Resource
from flask import request
from HR.models import team_model, organization_model
from HR import db
from google.cloud import firestore


api = Namespace('Team', description='Team related API')
@api.route('/')
class Team(Resource):
    @api.doc(description="Create new team")
    @api.expect(team_model, validate=True) 
    def post(self):
        team_info = api.payload
        orgnization_ID = 'n0sy1NF8qUHyy46b1gI9'
        org_ref = db.collection('organization').document(orgnization_ID)
        teams_ref = org_ref.collection('Teams').stream()
        for team in teams_ref:
            if team.to_dict()["Name"]== team_info['Name']:
                return {'message': 'Team Name already exists'}, 400


        org_ref.collection('Teams').add(team_info)
        return 'Team created successfully', 200

@api.route('/<string:team_name>')
class TeamInfo(Resource):
    @api.doc(description="Get Spisific  team information")
    def get(self,team_name):
        orgnization_ID = 'n0sy1NF8qUHyy46b1gI9'
        teams_ref = db.collection('organization').document(orgnization_ID).collection('Teams').stream()
        for team in teams_ref:
            if team.to_dict()["Name"]== team_name:
                return team.to_dict(), 200
        return {'message': 'Team not found'}, 404



    @api.doc(description="Update team information")
    @api.param('Name', 'New Team Name')
    @api.param('Description', 'New Team Description')
    def put(self,team_name):
        orgnization_ID = 'n0sy1NF8qUHyy46b1gI9'
        temas_ref = db.collection('organization').document(orgnization_ID).collection('Teams').stream()
        team_info = {}
        team_id = None
        for team in temas_ref:
            if team.to_dict()["Name"]== team_name:
                team_info = team.to_dict()
                team_id = team.id
                break
        if team_info == {}:
            return {'message': 'Team not found'}, 404
        if request.args.get("Name"):
            team_info['Name'] = request.args.get("Name")
        if request.args.get("Description"):
            team_info['Description'] = request.args.get("Description")
        db.collection('organization').document(orgnization_ID).collection('Teams').document(team_id).update(team_info)
   
    

        
@api.route('/<string:team_name>/employees')
class TeamEmployee(Resource):
    @api.doc(description="Get all employees in the team")
    def get(self,team_name):
        organization_id = 'n0sy1NF8qUHyy46b1gI9'
        teams_ref = db.collection('organization').document(organization_id).collection('Teams').stream()
        team_id = None
        for team in teams_ref:
            if team.to_dict()["Name"]== team_name:
                team_id = team.id
                break
        if team_id == None:
            return {'message': 'Team not found'}, 404
        employees_ref = db.collection('organization').document(organization_id).collection('Employees').where('TeamID', '==', team_id).stream()
        employees = []
        for employee in employees_ref:
            emp_info = employee.to_dict()
            emp_info['TeamName'] = team_name
            emp_info['ID'] = employee.id
            employees.append(emp_info)
        return employees, 200

        




    @api.doc(description="Add employee to the team")
    @api.param('employee_id', 'Employee ID',strict=True)
    def post(self,team_name):
        organization_id = 'n0sy1NF8qUHyy46b1gI9'
        teams_ref = db.collection('organization').document(organization_id).collection('Teams').stream()
        team_info = {}
        team_id = None
        employee_id = request.args.get("employee_id")
        if  employee_id == None:
            return {'message': 'Missing parameters'}, 400
        for team in teams_ref:
            if team.to_dict()["Name"]== team_name:
                team_id = team.id
                break
        if team_id == None:
            return {'message': 'Team not found'}, 404

        employee_info = db.collection('organization').document(organization_id).collection('Employees').document(employee_id).get().to_dict()
        try :
            if employee_info['TeamID'] != None:
                return {'message': 'Employee already in team'}, 400
            elif employee_info['TeamID'] == team_id:
                return {'message': 'Employee already in team'}, 400
            else:
                raise KeyError
        except KeyError:
            employee_info['TeamID'] = team_id
            db.collection('organization').document(organization_id).collection('Employees').document(employee_id).update(employee_info)
            return 'Employee added to team', 200
        
    @api.doc(description="Remove employee from the team")
    @api.param('employee_id', 'Employee ID',strict=True)
    def delete(self,team_name):
        organization_id = 'n0sy1NF8qUHyy46b1gI9'
        employee_id = request.args.get("employee_id")
        if  employee_id == None:
            return {'message': 'Missing parameters'}, 400
        employee_info = db.collection('organization').document(organization_id).collection('Employees').document(employee_id).get().to_dict()
        try :
            if employee_info['TeamID'] == None:
                return {'message': 'Employee not in team'}, 400
        except KeyError:
            return {'message': 'Employee not in team'}, 400
        employee_info['TeamID'] = None
        db.collection('organization').document(organization_id).collection('Employees').document(employee_id).update(employee_info)
        return 'Employee removed from team', 200    
    