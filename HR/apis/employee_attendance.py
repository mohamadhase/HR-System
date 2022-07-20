# external imports
from flask_restx import Namespace, Resource
from flask import abort, request

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
    @api.response(200, 'Attendance found', Employee.attend_info)
    @api.response(404, 'Employee not found or attendance not found')
    @api.response(400, 'Bad Date')
    @api.response(401, 'Unauthorized')
    @Authentication.token_required
    def get(organization_id, self, employee_id):
        # validate employee id
        if not Employee.is_exists(organization_id, employee_id)[0]:
            abort(404, "Employee not found")
        # validate date
        attend_date = Employee.validate_date(request.args)
        attend_date['Date'] = Employee.dict_to_datetime(attend_date)
        # get employee attendance
        validate_attendace, attend_info = Employee.is_attend(
            organization_id, employee_id, attend_date)
        if not validate_attendace:
            abort(404, "Attendance not found")
        return attend_info, 200

    @api.doc(description="Update employee attendance", security='apikey')
    @api.param('Day', 'Day of the month', required=True)
    @api.param('Month', 'Month of the year', required=True)
    @api.param('Year', 'Year', required=True)
    @api.param('number_of_hours', 'Number of hours', required=True)
    @api.response(200, 'Attendance updated', Employee.attend_info)
    @api.response(404, 'Employee not found or attendance not found')
    @api.response(400, 'Bad Date or Bad Number of Hours')
    @api.response(401, 'Unauthorized')
    @Authentication.token_required
    def patch(organization_id, self, employee_id):
        # validate employee id
        if not Employee.is_exists(organization_id, employee_id)[0]:
            abort(404, "Employee not found")
        # validate date
        attend_date = Employee.validate_date(request.args)
        attend_date['Date'] = Employee.dict_to_datetime(attend_date)
        # validate the attendance date
        validate_attend, attend_date = Employee.is_attend(
            organization_id, employee_id, attend_date)
        if not validate_attend:
            abort(404, "Attendance not found")
        # validate number of hours
        try:
            attend_date['NumberOfHours'] = int(request.args['number_of_hours'])
        except ValueError:
            abort(400, "Bad number of hours")
        except KeyError:
            abort(400, "Number of hours is required")
        if attend_date['NumberOfHours'] <= 0 or attend_date['NumberOfHours'] > 24:
            abort(400, "Bad number of hours")
        # update employee attendance
        Employee.update_attend(organization_id, employee_id, attend_date)
        return attend_date, 200

    @api.doc(description="Delete employee attendance", params={'employee_id': 'Employee ID'}, security='apikey')
    @api.param('Day', 'Day of the month', required=True)
    @api.param('Month', 'Month of the year', required=True)
    @api.param('Year', 'Year', required=True)
    @api.response(200, 'Attendance deleted')
    @api.response(404, 'Employee not found or attendance not found')
    @api.response(400, 'Bad Date')
    @api.response(401, 'Unauthorized')
    @Authentication.token_required
    def delete(organization_id, self, employee_id):
        # validate employee id
        if not Employee.is_exists(organization_id, employee_id)[0]:
            abort(404, "Employee not found")
        # validate date
        attend_date = Employee.validate_date(request.args)
        attend_date['Date'] = Employee.dict_to_datetime(attend_date)
        # validate the attendance date
        validate_attend, attend_date = Employee.is_attend(
            organization_id, employee_id, attend_date)
        if not validate_attend:
            abort(404, "Attendance not found")
        # delete employee attendance
        Employee.delete_attend(organization_id, employee_id, attend_date)
        return 'Attend deleted', 200

    @api.doc(description="Add employee attendance", security='apikey')
    @api.expect(Employee.attend_info, validate=True)
    @api.response(200, 'Attendance added', Employee.attend_info)
    @api.response(404, 'Employee not found')
    @api.response(400, 'Bad Date Or Bad Number of Hours')
    @api.response(409, 'Attendance already exists')
    @api.response(401, 'Unauthorized')
    @Authentication.token_required
    def post(organization_id, self, employee_id):
        # get attendance info
        attend_info = api.payload
        # validate employee id
        if not Employee.is_exists(organization_id, employee_id)[0]:
            abort(404, "Employee not found")
        # validate date
        attend_date = Employee.validate_date(attend_info)
        attend_date['Date'] = Employee.dict_to_datetime(attend_info)
        # validate the number of hours
        try:
            attend_date['NumberOfHours'] = int(attend_info['NumberOfHours'])
        except ValueError:
            abort(400, "Bad number of hours")
        except KeyError:
            abort(400, "Number of hours is required")

        if attend_date['NumberOfHours'] <= 0 or attend_date['NumberOfHours'] > 24:
            abort(400, "Bad number of hours")

        # validate the attendance date
        if Employee.is_attend(organization_id, employee_id, attend_date)[0]:
            abort(409, "Attendance already exists")
        # add employee attendance
        Employee.add_attend_day(organization_id, employee_id, attend_date)
        return attend_date, 200
