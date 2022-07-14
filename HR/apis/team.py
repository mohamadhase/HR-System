# external imports
from flask_restx import Namespace, Resource
from flask import request
from flask import abort
# internal imports
from HR import db
from HR.models.Team import Team
from HR.models.Employee import Employee

api = Namespace('Team', description='Team related API')


@api.route('/')
class TeamCreation(Resource):
    @api.doc(description="Create new team")
    @api.expect(Team.team_info, validate=True)
    @api.response(201, 'Team created successfully', Team.team_info)
    @api.response(409, 'Team With Same Name Already Exists')
    @api.response(400, 'invalud team name')
    def post(self):
        # get organization ID
        orgnization_ID = 'n0sy1NF8qUHyy46b1gI9'
        # get team info from payload
        team_info = api.payload
        # check if team name is valid
        if Team.is_valid_name(orgnization_ID, team_info['Name']) != True:
            abort(400, 'invalid team name')
        # check if team name is already exists
        if Team.is_exists(orgnization_ID, team_info['Name'])[0]:
            abort(409, 'Team with this name already exists')
        # create team
        return Team.create(orgnization_ID, team_info), 201


@api.route('/<string:team_name>')
class TeamInfo(Resource):
    @api.doc(description="Get Spisific  team information")
    @api.response(200, 'Team Information', Team.team_info)
    @api.response(404, 'Team Not Found')
    def get(self, team_name):
        # get organization ID
        orgnization_ID = 'n0sy1NF8qUHyy46b1gI9'
        # check if team is exists
        is_exist, team_info = Team.is_exists(orgnization_ID, team_name)
        if is_exist == False:
            abort(404, 'Team not found')
        # return team info
        return team_info, 200

    @api.doc(description="Update team information")
    @api.param('Description', 'New Team Description')
    @api.response(200, 'Team Information Updated', Team.team_info)
    @api.response(404, 'Team Not Found')
    @api.response(400, 'Description is required')
    def patch(self, team_name):
        # get organization ID
        orgnization_ID = 'n0sy1NF8qUHyy46b1gI9'
        # check if team is exists
        is_exists, team_info = Team.is_exists(orgnization_ID, team_name)
        if not is_exists:
            abort(404, 'Team not found')
        # get the  new description
        if request.args.get("Description"):
            team_info['Description'] = request.args.get("Description")
        else:
            abort('400', 'Description is required')
        # update team info
        Team.update(orgnization_ID, team_name, team_info)

        return team_info, 200

    def delete(self, team_name):
        # get organization ID
        organization_ID = 'n0sy1NF8qUHyy46b1gI9'
        # check if the team is exists
        if not Team.is_exists(organization_ID, team_name)[0]:
            abort(404, 'Team not found')
        # delete team
        Team.delete(organization_ID, team_name)
        return 'Team Deleted', 200


@api.route('/<string:team_name>/employees')
class TeamEmployee(Resource):
    @api.doc(description="Get all employees in the team")
    @api.response(200, 'Employees in the team', [Employee.employee_info])
    @api.response(404, 'Team Not Found')
    def get(self, team_name):
        # get organization ID
        organization_id = 'n0sy1NF8qUHyy46b1gI9'
        # check if team is exists
        if Team.is_exists(organization_id, team_name)[0] == False:
            abort(404, 'Team not found')
        # get all employees in the team
        return Team.get_employees(organization_id, team_name), 200

    @api.doc(description="Add employee to the team")
    @api.param('employee_id', 'Employee ID', strict=True)
    @api.response(200, 'Employee added to the team')
    @api.response(404, 'Team Not Found OR Employee Not Found')
    @api.response(409, 'Employee Already in the team')
    def post(self, team_name):
        # get organization ID
        organization_id = 'n0sy1NF8qUHyy46b1gI9'
        # get employee ID
        employee_id = request.args.get("employee_id")
        # check employee id
        if employee_id == None:
            abort(400, 'employee_id is required')
        # check if the team is exists
        if Team.is_exists(organization_id, team_name)[0] == False:
            abort(404, 'Team not found')
        # check if employee is exists
        validate_employee, employee_info = Employee.is_exists(
            organization_id, employee_id)
        if not validate_employee:
            abort(404, 'Employee not found')
        # check if employee is already in the team
        if Employee.in_team(organization_id, employee_id):
            abort(409, 'Employee is already in the team')
        # add employee to the team
        Employee.add_to_team(organization_id, employee_id, team_name)
        return 'Employee added to the team', 200

    @api.doc(description="Remove employee from the team")
    @api.param('employee_id', 'Employee ID', strict=True)
    @api.response(200, 'Employee removed from the team', Employee.employee_info)
    @api.response(404, 'Team Not Found OR Employee Not Found')
    @api.response(409, 'Employee is not in the team')
    @api.response(400, 'employee_id is required')
    def delete(self, team_name):
        # get organization ID
        organization_id = 'n0sy1NF8qUHyy46b1gI9'
        # get employee ID
        employee_id = request.args.get("employee_id")
        # check employee id
        if employee_id == None:
            abort(400, 'employee_id is required')
        # check if the team is exists
        if not Team.is_exists(organization_id, team_name)[0]:
            abort(404, 'Team not found')
        # check if employee is exists
        validate_employee, employee_info = Employee.is_exists(
            organization_id, employee_id)
        if not validate_employee:
            abort(404, 'Employee not found')
        # check if employee is in the team
        try:
            if employee_info['TeamID'] != team_name:
                abort(409, 'Employee not in the team')
        except KeyError:
            abort(409, 'Employee not in the team')
        # remove employee from the team
        employee_info['TeamID'] = None
        # update employee in the database
        Employee.update(organization_id, employee_id, employee_info)
        return employee_info, 200
