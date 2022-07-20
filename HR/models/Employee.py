# external imports
import datetime
from email.policy import HTTP
from http import HTTPStatus
from typing import Tuple
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
    def is_exists(orgnization_ID: str, employee_ID: str) -> Tuple[bool, dict]:
        """check if employee is exists

        Args:
            orgnization_ID (str):  organization ID the employee belongs to
            employee_ID (str): employee ID to be checked for existence

        Returns:
            Tuple[bool,dict]: (true if employee is exists | false if not, employee info)
        """
        employee_ref = db.collection('Organization').document(
            orgnization_ID).collection('Employees').document(employee_ID)
        return employee_ref.get().exists, employee_ref.get().to_dict()

    @staticmethod
    def is_in_team(orgnization_ID: str, employee_ID: str) -> bool:
        """check if employee is in team

        Args:
            orgnization_ID (str): organization ID the employee belongs to
            employee_ID (str): employee ID to be checked for existence in team

        Returns:
            bool: true if employee is in team | false if not
        """
        try:
            team_id = db.collection('Organization').document(
                orgnization_ID).collection('Employees').document(employee_ID).get().to_dict()['TeamID']
        except KeyError:
            return False

        return team_id != '' and team_id != None

    @staticmethod
    def add_to_team(orgnization_ID: str, employee_ID: str, team_ID: str) -> None:
        """add employee to team if not already in team and update the team if employee is in team

        Args:
            orgnization_ID (str): organization ID the employee belongs to
            employee_ID (str): employee ID to be added to team
            team_ID (str): team ID to be added to employee
        """
        db.collection('Organization').document(orgnization_ID).collection(
            'Employees').document(employee_ID).update({'TeamID': team_ID})

    @staticmethod
    def update(orgnization_ID: str, employee_ID: str, employee_info: dict) -> None:
        """ update employee info in database 

        Args:
            orgnization_ID (str): organization ID the employee belongs to
            employee_ID (str): employee ID to be updated
            employee_info (dict): employee info to be updated
        """
        db.collection('Organization').document(orgnization_ID).collection(
            'Employees').document(employee_ID).update(employee_info)

    @staticmethod
    def delete(orgnization_ID: str, employee_ID: str) -> None:
        """ delete employee from database

        Args:
            orgnization_ID (str): organization ID the employee belongs to
            employee_ID (str): employee ID to be deleted
        """
        db.collection('Organization').document(orgnization_ID).collection(
            'Employees').document(employee_ID).delete()

    @staticmethod
    def create(orgnization_ID: str, employee_info: dict) -> dict:
        """ create new  employee in database

        Args:
            orgnization_ID (str): organization ID the new employee belongs to
            employee_info (dict): employee info to be created

        Returns:
            dict: employee info created in database
        """
        employee_ref = db.collection('Organization').document(
            orgnization_ID).collection('Employees').document(employee_info['ID'])
        employee_ref.set(employee_info)
        return employee_ref.get().to_dict()

    @staticmethod
    def validate_date(date: dict) -> dict:
        """ validate given date if it is valid or not

        Args:
            date (dict): date to be validated

        Returns:
            dict: validated date
        """
        date_dict = {}
        if not date.get('Day'):
            abort(HTTPStatus.BAD_REQUEST.value, {'error': 'Day is required'})
        if not date.get('Month'):
            abort(HTTPStatus.BAD_REQUEST.value, {'error': 'Month is required'})
        if not date.get('Year'):
            abort(HTTPStatus.BAD_REQUEST.value, {'error': 'Year is required'})
        date_dict['Day'] = int(date.get('Day'))
        date_dict['Month'] = int(date.get('Month'))
        date_dict['Year'] = int(date.get('Year'))
        if date_dict['Year'] == 0:
            abort(HTTPStatus.BAD_REQUEST.value, {'error': 'Year cannot be 0'})
        if date_dict['Month'] < 1 or date_dict['Month'] > 12:
            abort(HTTPStatus.BAD_REQUEST.value, {'error': 'Month must be between 1 and 12'})
        if date_dict['Day'] < 1 or date_dict['Day'] > 31:
            abort(HTTPStatus.BAD_REQUEST.value, {'error': 'Day must be between 1 and 31'})
        try:
            date = datetime.date(
                date_dict['Year'], date_dict['Month'], date_dict['Day'])
        except ValueError as e:
            abort(HTTPStatus.BAD_REQUEST.value, str(e.args[0]))
        return date_dict

    @staticmethod
    def dict_to_datetime(date_dict: dict) -> str:
        """convert given date to datetime string in format YYYY-MM-DD

        Args:
            date_dict (dict): date to be converted

        Returns:
            str: datetime string in format YYYY-MM-DD
        """
        try:
            return datetime.date(date_dict['Year'], date_dict['Month'], date_dict['Day']).isoformat()

        except ValueError as e:
            abort(HTTPStatus.BAD_REQUEST.value, {'error': str(e.args[0])})

    @staticmethod
    def is_attend(orgnization_ID: str, employee_ID: str, date: dict) -> Tuple[bool, dict]:
        """ check if employee is attendance on given date

        Args:
            orgnization_ID (str): organization ID the employee belongs to
            employee_ID (str): employee ID to be checked for attendance
            date (dict): date to be checked for attendance

        Returns:
            Tuple[bool,dict]: (true if employee is attendance on given date | false if not, attendance info)
        """
        attend_ref = db.collection('Organization').document(
            orgnization_ID).collection('Employees').document(employee_ID).collection('Attendance').document(date['Date'])
        return attend_ref.get().exists, attend_ref.get().to_dict()

    @staticmethod
    def add_attend_day(orgnization_ID: str, employee_ID: str, date: dict) -> None:
        """ add attendance on given date for given employee to database

        Args:
            orgnization_ID (str): organization ID the employee belongs to
            employee_ID (str): employee ID to be added attendance
            date (dict): date to be added attendance
        """
        attend_day_ref = db.collection('Organization').document(
            orgnization_ID).collection('Employees').document(employee_ID).collection('Attendance').document(date['Date'])
        attend_day_ref.set(date)

    @staticmethod
    def update_attend(orgnization_ID: str, employee_ID: str, date: dict) -> None:
        """ update attendance on given date for given employee to database

        Args:
            orgnization_ID (str): organization ID the employee belongs to
            employee_ID (str): employee ID to be updated attendance
            date (dict): date to be updated attendance
        """
        attend_ref = db.collection('Organization').document(
            orgnization_ID).collection('Employees').document(employee_ID).collection('Attendance').document(date['Date'])
        attend_ref.update(date)

    @staticmethod
    def delete_attend(orgnization_ID: str, employee_ID: str, date: dict) -> None:
        """ delete attendance on given date for given employee to database

        Args:
            orgnization_ID (str): organization ID the employee belongs to
            employee_ID (str): employee ID to be deleted attendance
            date (dict): date to be deleted attendance
        """
        attend_ref = db.collection('Organization').document(
            orgnization_ID).collection('Employees').document(employee_ID).collection('Attendance').document(date['Date'])
        attend_ref.delete()
