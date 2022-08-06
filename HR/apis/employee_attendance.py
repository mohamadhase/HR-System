# external imports
from flask_restx import Namespace, Resource
from flask import abort, request
from http import HTTPStatus 

# internal imports
from HR import db
from HR.models.Employee import Employee
from HR.models.Authentication import Authentication
from HR.models.Logger import create_logger
from HR.models.Organization import Organization
api = Namespace('Employee Attendance',
                description='Employee Attendance related APIs')
logger = create_logger(__name__)
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
        logger.info(f"GET /{organization_id}/employee/{employee_id}/attendance")
        # validate employee id
        if not Employee.is_exists(organization_id, employee_id)[0]:
            logger.error(f"Employee {employee_id} not found returning status code {HTTPStatus.NOT_FOUND.value}")
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Employee not found'})
        # validate date
        attend_date = Employee.validate_date(request.args)
        attend_date['Date'] = Employee.dict_to_datetime(attend_date)
        # get employee attendance
        validate_attendace, attend_info = Employee.is_attend(
            organization_id, employee_id, attend_date)
        if not validate_attendace:
            logger.error(f"Employee {employee_id} not found returning status code {HTTPStatus.NOT_FOUND.value}")
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Attendance not found'})
        logger.info(f'Request completed successfully returning HTTP status code:{HTTPStatus.OK.value}')
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
        logger.info(f"PATCH /{organization_id}/employee/{employee_id}/attendance")
        # validate employee id
        if not Employee.is_exists(organization_id, employee_id)[0]:
            logger.error(f"Employee {employee_id} not found returning status code {HTTPStatus.NOT_FOUND.value}")
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Employee not found'})
        # validate date
        attend_date = Employee.validate_date(request.args)
        attend_date['Date'] = Employee.dict_to_datetime(attend_date)
        # validate the attendance date
        validate_attend, attend_date = Employee.is_attend(
            organization_id, employee_id, attend_date)
        if not validate_attend:
            logger.error(f"Employee {employee_id} not found returning status code {HTTPStatus.NOT_FOUND.value}")
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Attendance not found'})
        # validate number of hours
        try:
            attend_date['NumberOfHours'] = int(request.args['number_of_hours'])
        except ValueError:
            logger.error(f"Invalid number of hours {request.args['number_of_hours']} returning status code {HTTPStatus.BAD_REQUEST.value}")
            abort(HTTPStatus.BAD_REQUEST.value, {'error':'Invalid number of hours'})
        except KeyError:
            logger.error(f"Number of hours not found returning status code {HTTPStatus.BAD_REQUEST.value}")
            abort(HTTPStatus.BAD_REQUEST.value, {'error':'Number of hours is required'})
        if attend_date['NumberOfHours'] <= 0 or attend_date['NumberOfHours'] > 24:
            logger.error(f"Invalid number of hours {request.args['number_of_hours']} returning status code {HTTPStatus.BAD_REQUEST.value}")
            abort(HTTPStatus.BAD_REQUEST.value, {'error':'Invalid number of hours'})
        # update employee attendance
        Employee.update_attend(organization_id, employee_id, attend_date)
        logger.info(f'Request completed successfully returning HTTP status code:{HTTPStatus.OK.value}')
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
        logger.info(f"DELETE /{organization_id}/employee/{employee_id}/attendance")
        # validate employee id
        if not Employee.is_exists(organization_id, employee_id)[0]:
            logger.error(f"Employee {employee_id} not found returning status code {HTTPStatus.NOT_FOUND.value}")
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Employee not found'})
        # validate date
        attend_date = Employee.validate_date(request.args)
        attend_date['Date'] = Employee.dict_to_datetime(attend_date)
        # validate the attendance date
        validate_attend, attend_date = Employee.is_attend(
            organization_id, employee_id, attend_date)
        if not validate_attend:
            logger.error(f'Attendance not found returning status code {HTTPStatus.NOT_FOUND.value}')
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Attendance not found'})
        # delete employee attendance
        Employee.delete_attend(organization_id, employee_id, attend_date)
        logger.info(f'Request completed successfully returning HTTP status code:{HTTPStatus.OK.value}')
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
        logger.info(f"POST /{organization_id}/employee/{employee_id}/attendance")
        # get attendance info
        attend_info = api.payload
        # validate employee id
        if not Employee.is_exists(organization_id, employee_id)[0]:
            logger.error(f"Employee {employee_id} not found returning status code {HTTPStatus.NOT_FOUND.value}")
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Employee not found'})
        # validate date
        attend_date = Employee.validate_date(attend_info)
        attend_date['Date'] = Employee.dict_to_datetime(attend_info)
        # validate the number of hours
        try:
            attend_date['NumberOfHours'] = int(attend_info['NumberOfHours'])
        except ValueError:
            logger.error(f"Invalid number of hours {attend_info['NumberOfHours']} returning status code {HTTPStatus.BAD_REQUEST.value}")
            abort(HTTPStatus.BAD_REQUEST.value, {'error':'Invalid number of hours'})
        except KeyError:
            logger.eror(f"Number of hours not found returning status code {HTTPStatus.BAD_REQUEST.value}")
            abort(HTTPStatus.BAD_REQUEST.value, {'error':'Number of hours is required'})

        if attend_date['NumberOfHours'] <= 0 or attend_date['NumberOfHours'] > 24:
            logger.error(f"Invalid number of hours {attend_info['NumberOfHours']} returning status code {HTTPStatus.BAD_REQUEST.value}")
            abort(HTTPStatus.BAD_REQUEST.value, {'error':'Invalid number of hours'})

        # validate the attendance date
        if Employee.is_attend(organization_id, employee_id, attend_date)[0]:
            logger.error(f'Attendance already exists returning status code {HTTPStatus.CONFLICT.value}')
            abort(HTTPStatus.CONFLICT.value, {'error':'Attendance already exists'})
        # add employee attendance
        Employee.add_attend_day(organization_id, employee_id, attend_date)
        logger.info(f'Request completed successfully returning HTTP status code:{HTTPStatus.OK.value}')
        return attend_date, HTTPStatus.OK.value
@api.route('/get_all_attend')
class GetAttend(Resource):
    @api.doc(description="Get all employee attendance", security='apikey')
    @api.response(HTTPStatus.OK.value, HTTPStatus.OK.phrase)
    @api.response(HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.phrase)
    @api.response(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.phrase)
    @api.response(HTTPStatus.UNAUTHORIZED.value, HTTPStatus.UNAUTHORIZED.phrase)
    @api.param('Day', 'Day of the month', required=True)
    @api.param('Month', 'Month of the year', required=True)
    @api.param('Year', 'Year', required=True)
    @Authentication.token_required
    def get(organization_id, self):
        logger.info(f"GET /{organization_id}/employee/attendance")
        res = {'Teams':[], 'Employees':[]}
        #get the date
        date = Employee.validate_date(request.args)
        date['Date'] = Employee.dict_to_datetime(date)
        
        # get all teams and employees
        org_info = Organization.get_info(organization_id,teams=True,employees=True)
        teams = org_info['Teams']
        employees = org_info['Employees']
        #for each team get all employees
        for team in teams:
            team['Employees'] = [employee for employee in employees if employee['TeamID'] == team['Name']]
            res['Teams'].append({'TeamName':team['Name'],'Attends':0})
        
        #for each employee check if he has attendance for the given date
        for team in teams:
            for employee in team['Employees']:
                attend = Employee.is_attend(organization_id, employee['ID'], date)
                if attend[0]==True:
                    #if he has attendance update the number of attendances for the team in the response and add the employee to the response
                    res['Teams'][teams.index(team)]['Attends'] += 1
                    res['Employees'].append({'ID':employee['ID'],'EmployeeName':employee['Name'],'TeamName':team['Name'],'Hours':attend[1]['NumberOfHours']})
        return res, HTTPStatus.OK.value
