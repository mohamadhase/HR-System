# external imports
import calendar
import datetime
from flask import abort
from flask_restx import fields
# internal imports
from HR import db
from HR import api


def check_date(date_dict):
    if date_dict['Year'] == 0:
        return 'Year is invalid'

    if date_dict['Month'] < 1 or date_dict['Month'] > 12:
        return 'Month is not valid'
    if date_dict['Day'] < 1 or date_dict['Day'] > 31:
        return 'Day is not valid'
    try:

        date = datetime.date(
            date_dict['Year'], date_dict['Month'], date_dict['Day'])
    except ValueError as e:
        return e.args[0]

    return True


def dict_to_datetime(date_dict):
    try:
        return datetime.date(date_dict['Year'], date_dict['Month'], date_dict['Day']).isoformat()

    except ValueError as e:
        return e.args[0]


def is_employee_exists(employee_id):
    pass


class organization():
    organization_info = api.model('organization_info',  {
        "Name": fields.String(required=True, description="Organization Name"),
        "Address": fields.String(required=True, description="Organization Address"),
    })
    
    team_model = api.model('Team',
                       {
                           "Name": fields.String(required=True, description="Team Name"),
                           "Description": fields.String(required=True, description="Team Description")
                       }, strict=True)
    @staticmethod
    def get_info(orgnization_ID, teams=False, employees=False):

        org_ref = db.collection('organization').document(orgnization_ID)
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
        print(orgnization_info)
        return orgnization_info
    
    @staticmethod
    def update(orgnization_ID, orgnization_info):
        org_ref = db.collection('organization').document(orgnization_ID)
        org_ref.update(orgnization_info)
        return org_ref.get().to_dict()

    @staticmethod
    def is_exists(orgnization_ID):
        org_ref = db.collection('organization').document(orgnization_ID)
        return org_ref.get().exists
    
    @staticmethod
    def get_teams(orgnization_ID):
        teams_ref = db.collection('organization').document(orgnization_ID).collection('Teams').stream()
        teams = []
        for team in teams_ref:
            teams.append(team.to_dict())
        return teams
