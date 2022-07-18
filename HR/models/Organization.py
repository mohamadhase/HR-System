# external imports
from flask_restx import fields
import hashlib


# internal imports
from HR import db
from HR import api


class Organization():
    Organization_info = api.model('Organization_info',  {
        "Name": fields.String(required=True, description="Organization Name"),
        "Address": fields.String(required=True, description="Organization Address"),
    })


    @staticmethod
    
    def get_info(orgnization_ID, teams=False, employees=False):

        org_ref = db.collection('Organization').document(orgnization_ID)
        orgnization_info = org_ref.get().to_dict()
        if int(teams) == 1:
            orgnization_teams_ref = org_ref.collection('Teams').stream()
            orgnization_teams = []
            for team in orgnization_teams_ref:
                orgnization_teams.append(team.to_dict())
            orgnization_info['Teams'] = orgnization_teams
        if int(employees) == 1:
            orgnization_employees_ref = org_ref.collection(
                'Employees').stream()
            orgnization_employees = []
            for employee in orgnization_employees_ref:
                orgnization_employees.append(employee.to_dict())
            orgnization_info['Employees'] = orgnization_employees
        return orgnization_info

    @staticmethod
    def update(orgnization_ID, orgnization_info):
        org_ref = db.collection('Organization').document(orgnization_ID)
        org_ref.update(orgnization_info)
        return org_ref.get().to_dict()

    @staticmethod
    def is_exists(orgnization_ID):
        org_ref = db.collection('Organization').document(orgnization_ID)        
        return org_ref.get().exists

    @staticmethod
    def get_teams(orgnization_ID):
        teams_ref = db.collection('Organization').document(
            orgnization_ID).collection('Teams').stream()
        teams = [team.to_dict() for team in teams_ref]
        return teams

        
       