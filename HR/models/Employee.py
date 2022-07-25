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
from HR.models.Logger import create_logger
logger = create_logger(__name__)
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
        logger.info(f'Checking if Employee {employee_ID} exists')
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
        logger.info(f'Checking if Employee {employee_ID} is in team')
        try:
            team_id = db.collection('Organization').document(
                orgnization_ID).collection('Employees').document(employee_ID).get().to_dict()['TeamID']
        except KeyError:
            return False

        return team_id not in ['', None]

    @staticmethod
    def add_to_team(orgnization_ID: str, employee_ID: str, team_ID: str) -> None:
        """add employee to team if not already in team and update the team if employee is in team

        Args:
            orgnization_ID (str): organization ID the employee belongs to
            employee_ID (str): employee ID to be added to team
            team_ID (str): team ID to be added to employee
        """
        logger.info(f'Adding Employee {employee_ID} to team {team_ID}')
        db.collection('Organization').document(orgnization_ID).collection(
            'Employees').document(employee_ID).update({'TeamID': team_ID})
        logger.info(f'Employee {employee_ID} added to team {team_ID}')

    @staticmethod
    def update(orgnization_ID: str, employee_ID: str, employee_info: dict) -> None:
        """ update employee info in database 

        Args:
            orgnization_ID (str): organization ID the employee belongs to
            employee_ID (str): employee ID to be updated
            employee_info (dict): employee info to be updated
        """
        logger.info(f'Updating Employee {employee_ID}')
        db.collection('Organization').document(orgnization_ID).collection(
            'Employees').document(employee_ID).update(employee_info)
        logger.info(f'Employee {employee_ID} updated')

    @staticmethod
    def delete(orgnization_ID: str, employee_ID: str) -> None:
        """ delete employee from database

        Args:
            orgnization_ID (str): organization ID the employee belongs to
            employee_ID (str): employee ID to be deleted
        """
        logger.info(f'Deleting Employee {employee_ID}')
        db.collection('Organization').document(orgnization_ID).collection(
            'Employees').document(employee_ID).delete()
        logger.info(f'Employee {employee_ID} deleted')

    @staticmethod
    def create(orgnization_ID: str, employee_info: dict) -> dict:
        """ create new  employee in database

        Args:
            orgnization_ID (str): organization ID the new employee belongs to
            employee_info (dict): employee info to be created

        Returns:
            dict: employee info created in database
        """
        logger.info('Creating new Employee')
        employee_ref = db.collection('Organization').document(
            orgnization_ID).collection('Employees').document(employee_info['ID'])
        employee_ref.set(employee_info)
        logger.info(f'Employee {employee_info["ID"]} created')
        return employee_ref.get().to_dict()

    @staticmethod
    def validate_date(date: dict) -> dict:
        """ validate given date if it is valid or not

        Args:
            date (dict): date to be validated

        Returns:
            dict: validated date
        """
        logger.info(f'Validate date {date}')
        if not date.get('Day'):
            logger.error(f'Day is not provided Returning Error Code {HTTPStatus.BAD_REQUEST}')
            abort(HTTPStatus.BAD_REQUEST.value, {'error': 'Day is required'})
        if not date.get('Month'):
            logger.error(f'Month is not provided Returning Error Code {HTTPStatus.BAD_REQUEST}')
            abort(HTTPStatus.BAD_REQUEST.value, {'error': 'Month is required'})
        if not date.get('Year'):
            logger.error(f'Year is not provided Returning Error Code {HTTPStatus.BAD_REQUEST}')
            abort(HTTPStatus.BAD_REQUEST.value, {'error': 'Year is required'})
        date_dict = {'Day': int(date.get('Day')), 'Month': int(date.get('Month')), 'Year': int(date.get('Year'))}

        if date_dict['Year'] == 0:
            logger.error(f'Year cannot be 0 Returning Error Code {HTTPStatus.BAD_REQUEST}')
            abort(HTTPStatus.BAD_REQUEST.value, {'error': 'Year cannot be 0'})
        if date_dict['Month'] < 1 or date_dict['Month'] > 12:
            logger.error(f'Month must be between 1 and 12 Returning Error Code {HTTPStatus.BAD_REQUEST}')
            abort(HTTPStatus.BAD_REQUEST.value, {'error': 'Month must be between 1 and 12'})
        if date_dict['Day'] < 1 or date_dict['Day'] > 31:
            logger.error(f'Day must be between 1 and 31 Returning Error Code {HTTPStatus.BAD_REQUEST}')
            abort(HTTPStatus.BAD_REQUEST.value, {'error': 'Day must be between 1 and 31'})
        try:
            date = datetime.date(
                date_dict['Year'], date_dict['Month'], date_dict['Day'])
        except ValueError as e:
            logger.exception(f'Invalid Date {e} Returning Error Code {HTTPStatus.BAD_REQUEST}')
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
        logger.info(f'Converting date {date_dict} to datetime string')
        try:
            return datetime.date(date_dict['Year'], date_dict['Month'], date_dict['Day']).isoformat()

        except ValueError as e:
            logger.exception(f'Invalid Date {e} Returning Error Code {HTTPStatus.BAD_REQUEST}')
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
        logger.info(f'Checking if employee {employee_ID} is attendance on {date}')
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
        logger.info(f'Adding attendance on {date["Date"]} for employee {employee_ID}')
        attend_day_ref = db.collection('Organization').document(
            orgnization_ID).collection('Employees').document(employee_ID).collection('Attendance').document(date['Date'])
        attend_day_ref.set(date)
        logger.info(f'Attendance on {date["Date"]} for employee {employee_ID} added')

    @staticmethod
    def update_attend(orgnization_ID: str, employee_ID: str, date: dict) -> None:
        """ update attendance on given date for given employee to database

        Args:
            orgnization_ID (str): organization ID the employee belongs to
            employee_ID (str): employee ID to be updated attendance
            date (dict): date to be updated attendance
        """
        logger.info(f'Updating attendance on {date["Date"]} for employee {employee_ID}')
        attend_ref = db.collection('Organization').document(
            orgnization_ID).collection('Employees').document(employee_ID).collection('Attendance').document(date['Date'])
        attend_ref.update(date)
        logger.info(f'Attendance on {date["Date"]} for employee {employee_ID} updated')

    @staticmethod
    def delete_attend(orgnization_ID: str, employee_ID: str, date: dict) -> None:
        """ delete attendance on given date for given employee to database

        Args:
            orgnization_ID (str): organization ID the employee belongs to
            employee_ID (str): employee ID to be deleted attendance
            date (dict): date to be deleted attendance
        """
        logger.info(f'Deleting attendance on {date["Date"]} for employee {employee_ID}')
        attend_ref = db.collection('Organization').document(
            orgnization_ID).collection('Employees').document(employee_ID).collection('Attendance').document(date['Date'])
        attend_ref.delete()
        logger.info(f'Attendance on {date["Date"]} for employee {employee_ID} deleted')
