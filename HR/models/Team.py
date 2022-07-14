# external imports
from flask_restx import fields
# internal imports
from HR import db
from HR import api


class Team:
    team_info = api.model('Team',
                          {
                              "Name": fields.String(required=True, description="Team Name"),
                              "Description": fields.String(required=True, description="Team Description")
                          }, strict=True)

    @staticmethod
    def create(orgnization_ID, team_info):
        team_ref = db.collection('Organization').document(
            orgnization_ID).collection('Teams').document(team_info['Name'])

        team_ref.set(team_info)
        return team_ref.get().to_dict()

    @staticmethod
    def is_exists(orgnization_ID, team_ID):
        team_ref = db.collection('Organization').document(
            orgnization_ID).collection('Teams').document(team_ID)
        return team_ref.get().exists, team_ref.get().to_dict()

    @staticmethod
    def is_valid_name(team_name):
        return team_name != ''

    @staticmethod
    def update(orgnization_ID, team_name, team_info):
        db.collection('Organization').document(orgnization_ID).collection(
            'Teams').document(team_name).update(team_info)
    
    @staticmethod
    def get_employees(orgnization_ID, team_name):
        employees_ref = db.collection('Organization').document(orgnization_ID).collection(
            'Employees').where('TeamID', '==', team_name).stream()
        employees = [employee.to_dict() for employee in employees_ref]
        return employees

    @staticmethod
    def delete(orgnization_ID, team_name):
        # remove all the employees from the team
        employee_ref = db.collection('Organization').document(
            orgnization_ID).collection('Employees').where('TeamID', '==', team_name)
        for employee in employee_ref.stream():
            db.collection('Organization').document(orgnization_ID).collection(
                'Employees').document(employee.id).update({'TeamID': None})
        # remove the team
        team_ref = db.collection('Organization').document(
            orgnization_ID).collection('Teams').document(team_name)
        team_ref.delete()
