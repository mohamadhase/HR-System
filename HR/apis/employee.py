# external imports
from flask_restx import Namespace, Resource
from flask import request
from flask import abort

# internal imports
from HR import db
from HR.models.Team import Team
from HR.models.Employee import Employee
from HR.models.Authentication import Authentication

# intialize namespace for the Employee API
api = Namespace('Employee', description='Employee related APIs')


@api.route('/<string:employee_id>')
class EmployeeInfo(Resource):
    @api.doc(description="Get Spisific  employee information", security='apikey')
    @api.response(200, 'Employee Information', Employee.employee_info)
    @api.response(404, 'Employee Not Found')
    @api.response(401, 'Unauthorized')
    @Authentication.token_required
    def get(organization_id, self, employee_id):
        # check if employee is exists
        validate_employee, employee_info = Employee.is_exists(
            organization_id, employee_id)
        if not validate_employee:
            abort(404, 'Employee not found')
        # return employee info
        return employee_info, 200

    @api.doc(description="Update employee information", security='apikey')
    @api.param('employee_name', 'Employee Name')
    @api.param('employee_email', 'Employee Email')
    @api.param('employee_phone', 'Employee Phone')
    @api.param('employee_address', 'Employee Address')
    @api.param('employee_team_id', 'Employee TeamID')
    @api.response(200, 'Employee Information', Employee.employee_info)
    @api.response(404, 'Employee Not Found OR Team Not Found')
    @api.response(401, 'Unauthorized')
    @Authentication.token_required
    def put(organization_id, self, employee_id):
        # check if employee is exists
        validate_employee, employee_info = Employee.is_exists(
            organization_id, employee_id)
        if not validate_employee:
            abort(404, 'Employee not found')
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
                abort(404, 'Team not found')
        # update employee info
        Employee.update(organization_id, employee_id, employee_info)
        return employee_info, 200

    @api.doc(description="Delete employee", security='apikey')
    @api.response(404, 'Employee Not Found')
    @api.response(200, 'Employee Deleted')
    @api.response(401, 'Unauthorized')
    @Authentication.token_required
    def delete(organization_id, self, employee_id):
        # check if employee is exists
        if not Employee.is_exists(organization_id, employee_id)[0]:
            abort(404, 'Employee not found')
        # delete employee
        Employee.delete(organization_id, employee_id)
        return 'Employee Deleted', 200


@api.route('/')
class Employees(Resource):
    @api.doc(description="Create new employee", security='apikey')
    @api.expect(Employee.employee_info, validate=True)
    @api.response(200, 'Employee Created', Employee.employee_info)
    @api.response(404, 'Team Not Found ')
    @api.response(409, 'Employee Already Exists')
    @api.response(401, 'Unauthorized')
    @Authentication.token_required
    def post(organization_id, self):
        # get new employee information
        employee_info = api.payload
        # check if the employee is exists
        if Employee.is_exists(organization_id, employee_info['ID'])[0]:
            abort(409, 'Employee already exists')
        # chcek if the team is exists
        try:
            if not Team.is_exists(organization_id, employee_info['TeamID'])[0]:
                abort(404, 'Team not found')
        except KeyError:
            # if team is not exists, set team id to None
            employee_info['TeamID'] = None
        # create new employee
        return Employee.create(organization_id, employee_info), 200
