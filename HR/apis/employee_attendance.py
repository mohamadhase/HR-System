# external imports
from flask_restx import Namespace, Resource
from flask import abort, request
from http import HTTPStatus 

# internal imports
from HR import db
from HR.models.Employee import Employee
from HR.models.Authentication import Authentication
api = Namespace('Employee Attendance',
                description='Employee Attendance related APIs')


@api.route('/<string:employee_id>/attendance')
class EmployeeAttendance(Resource):
    @api.doc(description="Get Spisific  employee attendance", security='apikey')
    @api.param('Day', 'Day of the month')
    @api.param('Month', 'Month of the year')
    @api.param('Year', 'Year')
    @api.response(HTTPStatus.OK.value, HTTPStatus.OK.phrase, Employee.attend_info)
    @api.response(HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.phrase)
    @api.response(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.phrase)
    @api.response(HTTPStatus.UNAUTHORIZED.value, HTTPStatus.UNAUTHORIZED.phrase)
    @Authentication.token_required
    def get(organization_id, self, employee_id):
        # validate employee id
        if not Employee.is_exists(organization_id, employee_id)[0]:
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Employee not found'})
        # validate date
        attend_date = Employee.validate_date(request.args)
        attend_date['Date'] = Employee.dict_to_datetime(attend_date)
        # get employee attendance
        validate_attendace, attend_info = Employee.is_attend(
            organization_id, employee_id, attend_date)
        if not validate_attendace:
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Attendance not found'})
        return attend_info, HTTPStatus.OK.value

    @api.doc(description="Update employee attendance", security='apikey')
    @api.param('Day', 'Day of the month', required=True)
    @api.param('Month', 'Month of the year', required=True)
    @api.param('Year', 'Year', required=True)
    @api.param('number_of_hours', 'Number of hours', required=True)
    @api.response(HTTPStatus.OK.value, HTTPStatus.OK.phrase, Employee.attend_info)
    @api.response(HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.phrase)
    @api.response(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.phrase)
    @api.response(HTTPStatus.UNAUTHORIZED.value, HTTPStatus.UNAUTHORIZED.phrase)
    @Authentication.token_required
    def patch(organization_id, self, employee_id):
        # validate employee id
        if not Employee.is_exists(organization_id, employee_id)[0]:
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Employee not found'})
        # validate date
        attend_date = Employee.validate_date(request.args)
        attend_date['Date'] = Employee.dict_to_datetime(attend_date)
        # validate the attendance date
        validate_attend, attend_date = Employee.is_attend(
            organization_id, employee_id, attend_date)
        if not validate_attend:
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Attendance not found'})
        # validate number of hours
        try:
            attend_date['NumberOfHours'] = int(request.args['number_of_hours'])
        except ValueError:
            abort(HTTPStatus.BAD_REQUEST.value, {'error':'Invalid number of hours'})
        except KeyError:
            abort(HTTPStatus.BAD_REQUEST.value, {'error':'Number of hours is required'})
        if attend_date['NumberOfHours'] <= 0 or attend_date['NumberOfHours'] > 24:
            abort(HTTPStatus.BAD_REQUEST.value, {'error':'Invalid number of hours'})
        # update employee attendance
        Employee.update_attend(organization_id, employee_id, attend_date)
        return attend_date, HTTPStatus.OK.value

    @api.doc(description="Delete employee attendance", params={'employee_id': 'Employee ID'}, security='apikey')
    @api.param('Day', 'Day of the month', required=True)
    @api.param('Month', 'Month of the year', required=True)
    @api.param('Year', 'Year', required=True)
    @api.response(HTTPStatus.OK.value, HTTPStatus.OK.phrase, Employee.attend_info)
    @api.response(HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.phrase)
    @api.response(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.phrase)
    @api.response(HTTPStatus.UNAUTHORIZED.value, HTTPStatus.UNAUTHORIZED.phrase)
    @Authentication.token_required
    def delete(organization_id, self, employee_id):
        # validate employee id
        if not Employee.is_exists(organization_id, employee_id)[0]:
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Employee not found'})
        # validate date
        attend_date = Employee.validate_date(request.args)
        attend_date['Date'] = Employee.dict_to_datetime(attend_date)
        # validate the attendance date
        validate_attend, attend_date = Employee.is_attend(
            organization_id, employee_id, attend_date)
        if not validate_attend:
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Attendance not found'})
        # delete employee attendance
        Employee.delete_attend(organization_id, employee_id, attend_date)
        return 'Attend deleted', HTTPStatus.OK.value

    @api.doc(description="Add employee attendance", security='apikey')
    @api.expect(Employee.attend_info, validate=True)
    @api.response(HTTPStatus.OK.value, HTTPStatus.OK.phrase, Employee.attend_info)
    @api.response(HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.phrase)
    @api.response(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.phrase)
    @api.response(HTTPStatus.CONFLICT.value, HTTPStatus.CONFLICT.phrase)
    @api.response(HTTPStatus.UNAUTHORIZED.value, HTTPStatus.UNAUTHORIZED.phrase)
    @Authentication.token_required
    def post(organization_id, self, employee_id):
        # get attendance info
        attend_info = api.payload
        # validate employee id
        if not Employee.is_exists(organization_id, employee_id)[0]:
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Employee not found'})
        # validate date
        attend_date = Employee.validate_date(attend_info)
        attend_date['Date'] = Employee.dict_to_datetime(attend_info)
        # validate the number of hours
        try:
            attend_date['NumberOfHours'] = int(attend_info['NumberOfHours'])
        except ValueError:
            abort(HTTPStatus.BAD_REQUEST.value, {'error':'Invalid number of hours'})
        except KeyError:
            abort(HTTPStatus.BAD_REQUEST.value, {'error':'Number of hours is required'})

        if attend_date['NumberOfHours'] <= 0 or attend_date['NumberOfHours'] > 24:
            abort(HTTPStatus.BAD_REQUEST.value, {'error':'Invalid number of hours'})

        # validate the attendance date
        if Employee.is_attend(organization_id, employee_id, attend_date)[0]:
            abort(HTTPStatus.CONFLICT.value, {'error':'Attendance already exists'})
        # add employee attendance
        Employee.add_attend_day(organization_id, employee_id, attend_date)
        return attend_date, HTTPStatus.OK.value
