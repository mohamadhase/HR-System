# external imports
import datetime
from flask import abort
from flask_restx import fields
# internal imports
from HR import db
from HR import api


class Employee:
    employee_info = api.model('Employee', {
        "ID": fields.String(required=True, description="Employee ID"),
        "Name": fields.String(required=True, description="Employee Name"),
        "Email": fields.String(required=True, description="Employee Email"),
        "Phone": fields.String(required=True, description="Employee Phone"),
        "Addres": fields.String(required=True, description="Employee Address"),
        "TeamID": fields.String(required=False, description="Employee TeamID"),
    }, strict=True)
    attend_info = api.model('Employee Attendance', {
        "Day": fields.Integer(required=True, description="Attendance Day"),
        "Month": fields.Integer(required=True, description="Attendance Date"),
        "Year": fields.Integer(required=True, description="Attendance Year"),
        "NumberOfHours": fields.Integer(required=True, description="Number of Hours")
    }, strict=True)

    @staticmethod
    def is_exists(orgnization_ID, employee_ID):
        employee_ref = db.collection('Organization').document(
            orgnization_ID).collection('Employees').document(employee_ID)
        return employee_ref.get().exists, employee_ref.get().to_dict()

    @staticmethod
    def in_team(orgnization_ID, employee_ID):
        try:
            team_id = db.collection('Organization').document(
                orgnization_ID).collection('Employees').document(employee_ID).get().to_dict()['TeamID']
        except KeyError:
            return False

        return team_id != '' and team_id != None

    @staticmethod
    def add_to_team(orgnization_ID, employee_ID, team_ID):
        db.collection('Organization').document(orgnization_ID).collection(
            'Employees').document(employee_ID).update({'TeamID': team_ID})

    @staticmethod
    def update(orgnization_ID, employee_ID, employee_info):
        db.collection('Organization').document(orgnization_ID).collection(
            'Employees').document(employee_ID).update(employee_info)

    @staticmethod
    def delete(orgnization_ID, employee_ID):
        db.collection('Organization').document(orgnization_ID).collection(
            'Employees').document(employee_ID).delete()

    @staticmethod
    def create(orgnization_ID, employee_info):
        employee_ref = db.collection('Organization').document(
            orgnization_ID).collection('Employees').document(employee_info['ID'])
        employee_ref.set(employee_info)
        return employee_ref.get().to_dict()

    @staticmethod
    def validate_date(date):
        date_dict = {}
        if not date.get('Day'):
            abort(400, "Missing day")
        if not date.get('Month'):
            abort(400, "Missing month")
        if not date.get('Year'):
            abort(400, "Missing year")
        date_dict['Day'] = int(date.get('Day'))
        date_dict['Month'] = int(date.get('Month'))
        date_dict['Year'] = int(date.get('Year'))
        if date_dict['Year'] == 0:
            abort(400, "Invalid year")
        if date_dict['Month'] < 1 or date_dict['Month'] > 12:
            abort(400, "Invalid month")
        if date_dict['Day'] < 1 or date_dict['Day'] > 31:
            abort(400, "Invalid day")
        try:
            date = datetime.date(
                date_dict['Year'], date_dict['Month'], date_dict['Day'])
        except ValueError as e:
            abort(400, str(e.args[0]))
        return date_dict

    @staticmethod
    def dict_to_datetime(date_dict):
        try:
            return datetime.date(date_dict['Year'], date_dict['Month'], date_dict['Day']).isoformat()

        except ValueError as e:
            abort(400, str(e.args[0]))

    @staticmethod
    def is_attend(orgnization_ID, employee_ID, date):
        attend_ref = db.collection('Organization').document(
            orgnization_ID).collection('Employees').document(employee_ID).collection('Attendance').document(date['Date'])
        return attend_ref.get().exists, attend_ref.get().to_dict()

    @staticmethod
    def add_attend_day(orgnization_ID, employee_ID, date):
        attend_day_ref = db.collection('Organization').document(
            orgnization_ID).collection('Employees').document(employee_ID).collection('Attendance').document(date['Date'])
        attend_day_ref.set(date)

    @staticmethod
    def update_attend(orgnization_ID, employee_ID, date):
        attend_ref = db.collection('Organization').document(
            orgnization_ID).collection('Employees').document(employee_ID).collection('Attendance').document(date['Date'])
        attend_ref.update(date)

    @staticmethod
    def delete_attend(orgnization_ID, employee_ID, date):
        attend_ref = db.collection('Organization').document(
            orgnization_ID).collection('Employees').document(employee_ID).collection('Attendance').document(date['Date'])
        attend_ref.delete()
    @staticmethod 
    def get_all_employees(orgnization_ID):
        employees_ref = db.collection('Organization').document(
            orgnization_ID).collection('Employees').stream()
        employess = []
        for employee in employees_ref:
            employess.append(employee.to_dict())
        return employess

