# external imports
from flask_restx import Namespace, Resource
from flask import request
from flask import abort
# internal imports
from HR import db
from HR.models.Team import Team
from HR.models.Employee import Employee
from HR.models.Authentication import Authentication
from http import HTTPStatus

# initialize the namespace for the team API
api = Namespace('Team', description='Team related API')
@api.route('/')
class TeamCreation(Resource):
    @api.doc(description="Create new team",security='apikey')
    @api.expect(Team.team_info, validate=True)
    @api.response(HTTPStatus.CREATED.value, 'Team created successfully', Team.team_info)
    @api.response(HTTPStatus.CONFLICT, 'Team With Same Name Already Exists')
    @api.response(HTTPStatus.BAD_REQUEST, 'invalud team name')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Unauthorized')
    @Authentication.token_required
    def post(orgnization_ID,self):
        # get team info from payload
        team_info = api.payload
        # check if team name is valid
        if not Team.is_valid_name(team_info['Name']) :
            abort(HTTPStatus.BAD_REQUEST, 'invalid team name')
        # check if team name is already exists
        if Team.is_exists(orgnization_ID, team_info['Name'])[0]:
            abort(HTTPStatus.CONFLICT, 'Team with this name already exists')
        # create team
        return Team.create(orgnization_ID, team_info), 201


@api.route('/<string:team_name>')
class TeamInfo(Resource):
    @api.doc(description="Get Spisific  team information",security='apikey')
    @api.response(HTTPStatus.OK, 'Team Information', Team.team_info)
    @api.response(HTTPStatus.NOT_FOUND, 'Team Not Found')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Unauthorized')
    @Authentication.token_required
    def get(orgnization_ID,self, team_name):
        # check if team is exists
        is_exist, team_info = Team.is_exists(orgnization_ID, team_name)
        if not is_exist:
            abort(HTTPStatus.NOT_FOUND, 'Team not found')
        # return team info
        return team_info, HTTPStatus.OK

    @api.doc(description="Update team information",security='apikey')
    @api.param('Description', 'New Team Description')
    @api.response(HTTPStatus.OK, 'Team Information Updated', Team.team_info)
    @api.response(HTTPStatus.NOT_FOUND, 'Team Not Found')
    @api.response(HTTPStatus.BAD_REQUEST, 'Description is required')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Unauthorized')
    @Authentication.token_required
    def patch(orgnization_ID,self, team_name):
        # check if team is exists
        print("hi")
        is_exists, team_info = Team.is_exists(orgnization_ID, team_name)
        if not is_exists:
            abort(HTTPStatus.NOT_FOUND, 'Team not found')
        # get the new description
        if request.args.get("Description"):
            team_info['Description'] = request.args.get("Description")
        else:
            abort(HTTPStatus.BAD_REQUEST, 'Description is required')
        # update team info
        Team.update(orgnization_ID, team_name, team_info)
        # return team info
        return team_info, HTTPStatus.OK
    
    @api.doc(description="Delete team",security='apikey')
    @api.response(HTTPStatus.OK, 'Team Deleted')
    @api.response(HTTPStatus.NOT_FOUND, 'Team Not Found')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Unauthorized')
    @Authentication.token_required
    def delete(organization_ID,self, team_name):
        # check if the team is exists
        if not Team.is_exists(organization_ID, team_name)[0]:
            abort(HTTPStatus.NOT_FOUND, 'Team not found')
        # delete team
        Team.delete(organization_ID, team_name)
        return 'Team Deleted', HTTPStatus.OK


@api.route('/<string:team_name>/employees')
class TeamEmployee(Resource):
    @api.doc(description="Get all employees in the team",security='apikey')
    @api.response(HTTPStatus.OK, 'Employees in the team', [Employee.employee_info])
    @api.response(HTTPStatus.NOT_FOUND, 'Team Not Found')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Unauthorized')
    @Authentication.token_required
    def get(organization_id,self, team_name):
        # check if team is exists
        if Team.is_exists(organization_id, team_name)[0] == False:
            abort(HTTPStatus.NOT_FOUND, 'Team not found')
        # get all employees in the team
        return Team.get_employees(organization_id, team_name), HTTPStatus.OK

    @api.doc(description="Add employee to the team",security='apikey')
    @api.param('employee_id', 'Employee ID', strict=True)
    @api.response(HTTPStatus.OK, 'Employee added to the team')
    @api.response(HTTPStatus.NOT_FOUND, 'Team Not Found OR Employee Not Found')
    @api.response(HTTPStatus.CONFLICT, 'Employee Already in the team')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Unauthorized')
    @Authentication.token_required
    def post(organization_id,self, team_name):
        # get employee ID
        employee_id = request.args.get("employee_id")
        # check employee id
        if employee_id == None:
            abort(HTTPStatus.BAD_REQUEST, 'employee_id is required')
        # check if the team is exists
        if not Team.is_exists(organization_id, team_name)[0]:
            abort(HTTPStatus.NOT_FOUND, 'Team not found')
        # check if employee is exists
        validate_employee, employee_info = Employee.is_exists(
            organization_id, employee_id)
        if not validate_employee:
            abort(HTTPStatus.NOT_FOUND, 'Employee not found')
        # check if employee is already in the team
        if Employee.is_in_team(organization_id, employee_id):
            abort(HTTPStatus.CONFLICT, 'Employee is already in the team')
        # add employee to the team
        Employee.add_to_team(organization_id, employee_id, team_name)
        return 'Employee added to the team', HTTPStatus.OK

    @api.doc(description="Remove employee from the team",security='apikey')
    @api.param('employee_id', 'Employee ID', strict=True)
    @api.response(HTTPStatus.OK, 'Employee removed from the team', Employee.employee_info)
    @api.response(HTTPStatus.NOT_FOUND, 'Team Not Found OR Employee Not Found')
    @api.response(HTTPStatus.CONFLICT, 'Employee is not in the team')
    @api.response(HTTPStatus.BAD_REQUEST, 'employee_id is required')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Unauthorized')
    @Authentication.token_required
    def delete(organization_id,self, team_name):
        # get employee ID
        employee_id = request.args.get("employee_id")
        # check employee id
        if employee_id == None:
            abort(HTTPStatus.BAD_REQUEST, 'employee_id is required')
        # check if the team is exists
        if not Team.is_exists(organization_id, team_name)[0]:
            abort(HTTPStatus.NOT_FOUND, 'Team not found')
        # check if employee is exists
        validate_employee, employee_info = Employee.is_exists(
            organization_id, employee_id)
        if not validate_employee:
            abort(HTTPStatus.NOT_FOUND, 'Employee not found')
        # check if employee is in the team
        try:
            if employee_info['TeamID'] != team_name:
                abort(HTTPStatus.CONFLICT, 'Employee not in the team')
        except KeyError:
            abort(HTTPStatus.CONFLICT, 'Employee not in the team')
        # remove employee from the team
        employee_info['TeamID'] = None
        # update employee in the database
        Employee.update(organization_id, employee_id, employee_info)
        return employee_info, HTTPStatus.OK
