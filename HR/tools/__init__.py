# external imports
import calendar
import datetime
from flask import abort
from flask_restx import fields
from google.api_core.exceptions import InvalidArgument
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
        print(orgnization_info)
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

    def is_exists(orgnization_ID, team_ID):
        team_ref = db.collection('Organization').document(
            orgnization_ID).collection('Teams').document(team_ID)
        return team_ref.get().exists, team_ref.get().to_dict()

    def is_valid_name(orgnization_ID, team_name):
        return team_name != '' 

    def update(orgnization_ID, team_name, team_info):
        db.collection('Organization').document(orgnization_ID).collection(
            'Teams').document(team_name).update(team_info)
        
    def get_employees(orgnization_ID, team_name):
        employees_ref = db.collection('Organization').document(orgnization_ID).collection(
            'Employees').where('TeamID', '==', team_name).stream()
        employees = [employee.to_dict() for employee in employees_ref]
        return employees
    def delete(orgnization_ID,team_name):
        #remove all the employees from the team
        employee_ref = db.collection('Organization').document(orgnization_ID).collection('Employees').where('TeamID', '==', team_name)
        for employee in employee_ref.stream(): 
            db.collection('Organization').document(orgnization_ID).collection('Employees').document(employee.id).update({'TeamID':None})
        #remove the team
        team_ref = db.collection('Organization').document(orgnization_ID).collection('Teams').document(team_name)
        team_ref.delete()
        
    
    
class Employee:
    employee_info = api.model('Employee', {
    "ID": fields.String(required=True, description="Employee ID"),
    "Name": fields.String(required=True, description="Employee Name"),
    "Email": fields.String(required=True, description="Employee Email"),
    "Phone": fields.String(required=True, description="Employee Phone"),
    "Addres": fields.String(required=True, description="Employee Address"),
    "TeamID": fields.String(required=False, description="Employee TeamID"),
    }, strict=True)
    @staticmethod
    def is_exists(orgnization_ID, employee_ID):
        employee_ref = db.collection('Organization').document(
            orgnization_ID).collection('Employees').document(employee_ID)
        return employee_ref.get().exists , employee_ref.get().to_dict()
        
    def in_team(orgnization_ID, employee_ID):
        try :
            team_id = db.collection('Organization').document(
                orgnization_ID).collection('Employees').document(employee_ID).get().to_dict()['TeamID']
        except KeyError:
            return False
            
        return  team_id != '' and team_id != None
    def add_to_team(orgnization_ID, employee_ID, team_ID):
        db.collection('Organization').document(orgnization_ID).collection(
            'Employees').document(employee_ID).update({'TeamID': team_ID})
        
    def update(orgnization_ID, employee_ID, employee_info):
        db.collection('Organization').document(orgnization_ID).collection(
            'Employees').document(employee_ID).update(employee_info)