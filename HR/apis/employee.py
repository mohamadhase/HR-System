# external imports
from flask_restx import Namespace, Resource
from flask import request
from flask import abort
from http import HTTPStatus 

# internal imports
from HR import db
from HR.models.Team import Team
from HR.models.Employee import Employee
from HR.models.Authentication import Authentication
from HR.models.Logger import create_logger
# intialize namespace for the Employee API
api = Namespace('Employee', description='Employee related APIs')
logger = create_logger(__name__)

@api.route('/<string:employee_id>')
class EmployeeInfo(Resource):
    @api.doc(description="Get Spisific  employee information", security='apikey')
    @api.response(HTTPStatus.OK.value, HTTPStatus.OK.phrase, Employee.employee_info)
    @api.response(HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.phrase)
    @api.response(HTTPStatus.UNAUTHORIZED.value, HTTPStatus.UNAUTHORIZED.phrase)
    @Authentication.token_required
    def get(organization_id, self, employee_id):
        logger.info(f'Get /eployee/{employee_id}')
        # check if employee is exists
        validate_employee, employee_info = Employee.is_exists(
            organization_id, employee_id)
        if not validate_employee:
            logger.error(f'Employee {employee_id} does not exist')
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Employee not found'})
        # return employee info
        logger.info(f'Request completed successfully returning HTTP status code:{HTTPStatus.OK.value}')
        return employee_info, HTTPStatus.OK.value

    @api.doc(description="Update employee information", security='apikey')
    @api.param('employee_name', 'Employee Name')
    @api.param('employee_email', 'Employee Email')
    @api.param('employee_phone', 'Employee Phone')
    @api.param('employee_address', 'Employee Address')
    @api.param('employee_team_id', 'Employee TeamID')
    @api.response(HTTPStatus.OK.value, HTTPStatus.OK.phrase, Employee.employee_info)
    @api.response(HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.phrase)
    @api.response(HTTPStatus.UNAUTHORIZED.value, HTTPStatus.UNAUTHORIZED.phrase)
    @Authentication.token_required
    def put(organization_id, self, employee_id):
        logger.info(f'Put /eployee/{employee_id}')
        # check if employee is exists
        validate_employee, employee_info = Employee.is_exists(
            organization_id, employee_id)
        if not validate_employee:
            logger.error(f'Employee {employee_id} does not exist returning HTTP status code:{HTTPStatus.NOT_FOUND.value}')
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Employee not found'})
        # get new information
        if request.args.get('employee_name'):
            employee_info['Name'] = request.args.get('employee_name')
        if request.args.get('employee_email'):
            employee_info['Email'] = request.args.get('employee_email')
        if request.args.get('employee_phone'):
            employee_info['Phone'] = request.args.get('employee_phone')
        if request.args.get('employee_address'):
            employee_info['Address'] = request.args.get('employee_address')
        if request.args.get('employee_team_id'):
            # check if the team is exists
            if Team.is_exists(organization_id, request.args.get('employee_team_id'))[0]:
                employee_info['TeamID'] = request.args.get('employee_team_id')
            else:
                logger.error(f"Team {request.args.get('employee_team_id')} does not exist returning HTTP status code:{HTTPStatus.NOT_FOUND.value}")
                abort(HTTPStatus.NOT_FOUND.value, {'error':'Team not found'})
        # update employee info
        Employee.update(organization_id, employee_id, employee_info)
        logger.info(f'Request completed successfully returning HTTP status code:{HTTPStatus.OK.value}')
        return employee_info, HTTPStatus.OK.value

    @api.doc(description="Delete employee", security='apikey')
    @api.response(HTTPStatus.OK.value, HTTPStatus.OK.phrase)
    @api.response(HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.phrase)
    @api.response(HTTPStatus.UNAUTHORIZED.value, HTTPStatus.UNAUTHORIZED.phrase)
    @Authentication.token_required
    def delete(organization_id, self, employee_id):
        logger.info(f'Delete /eployee/{employee_id}')
        # check if employee is exists
        if not Employee.is_exists(organization_id, employee_id)[0]:
            logger.error(f'Employee {employee_id} does not exist returning HTTP status code:{HTTPStatus.NOT_FOUND.value}')
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Employee not found'})
        # delete employee
        Employee.delete(organization_id, employee_id)
        logger.info(f'Request completed successfully returning HTTP status code:{HTTPStatus.OK.value}')
        return 'Employee Deleted', HTTPStatus.OK.value


@api.route('/')
class Employees(Resource):
    @api.doc(description="Create new employee", security='apikey')
    @api.expect(Employee.employee_info, validate=True)
    @api.response(HTTPStatus.OK.value, HTTPStatus.OK.phrase, Employee.employee_info)
    @api.response(HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.phrase)
    @api.response(HTTPStatus.CONFLICT.value, HTTPStatus.CONFLICT.phrase)
    @api.response(HTTPStatus.UNAUTHORIZED.value, HTTPStatus.UNAUTHORIZED.phrase)
    @Authentication.token_required
    def post(organization_id, self):
        logger.info(f'Post /eployee')
        # get new employee information
        employee_info = api.payload
        # check if the employee is exists
        if Employee.is_exists(organization_id, employee_info['ID'])[0]:
            logger.error(f'Employee {employee_info["ID"]} already exists returning HTTP status code:{HTTPStatus.CONFLICT.value}')
            abort(HTTPStatus.CONFLICT.value, {'error':'Employee already exists'})
        # chcek if the team is exists
        try:
            if not Team.is_exists(organization_id, employee_info['TeamID'])[0]:
                logger.error(f"Team {employee_info['TeamID']} does not exist returning HTTP status code:{HTTPStatus.NOT_FOUND.value}")
                abort(HTTPStatus.NOT_FOUND.value, {'error':'Team not found'})
        except KeyError:
            # if team is not exists, set team id to None
            employee_info['TeamID'] = None
        # create new employee
        Employee.create(organization_id, employee_info)
        logger.info(f'Request completed successfully returning HTTP status code:{HTTPStatus.OK.value}')
        return employee_info, HTTPStatus.OK.value
