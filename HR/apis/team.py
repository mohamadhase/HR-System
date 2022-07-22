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
from HR.models.Logger import *
# initialize the namespace for the team API
api = Namespace('Team', description='Team related API')
# initialize the logger
logger = create_logger(__name__)
@api.route('/')
class TeamCreation(Resource):
    @api.doc(description="Create new team",security='apikey')
    @api.expect(Team.team_info, validate=True)
    @api.response(HTTPStatus.CREATED.value, HTTPStatus.CREATED.phrase, Team.team_info)
    @api.response(HTTPStatus.CONFLICT.value, HTTPStatus.CONFLICT.phrase)
    @api.response(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.phrase)
    @api.response(HTTPStatus.UNAUTHORIZED.value, HTTPStatus.UNAUTHORIZED.phrase)
    @Authentication.token_required
    def post(orgnization_ID,self):
        logger.info('POST /team/')
        # get team info from payload
        team_info = api.payload
        # check if team name is valid
        if not Team.is_valid_name(team_info['Name']) :
            logger.error(f'{team_info["Name"]} is not a valid team name returning {HTTPStatus.BAD_REQUEST}')
            abort(HTTPStatus.BAD_REQUEST.value, {'error':'invalid team name'})
        # check if team name is already exists
        if Team.is_exists(orgnization_ID, team_info['Name'])[0]:
            logger.error(f'{team_info["Name"]} is already exists returning {HTTPStatus.CONFLICT}')
            abort(HTTPStatus.CONFLICT.value, {'error':'Team with this name already exists'})
        # create team
        team_info = Team.create(orgnization_ID, team_info)
        logger.info(f'Request completed successfully returning HTTP status code:{HTTPStatus.CREATED.value}')
        return team_info, HTTPStatus.CREATED.value


@api.route('/<string:team_name>')
class TeamInfo(Resource):
    @api.doc(description="Get Spisific  team information",security='apikey')
    @api.response(HTTPStatus.OK.value, HTTPStatus.OK.phrase, Team.team_info)
    @api.response(HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.phrase)
    @api.response(HTTPStatus.UNAUTHORIZED.value, HTTPStatus.UNAUTHORIZED.phrase)
    @Authentication.token_required
    def get(orgnization_ID,self, team_name):
        logger.info(f'GET /team/{team_name}')
        # check if team is exists
        is_exist, team_info = Team.is_exists(orgnization_ID, team_name)
        if not is_exist:
            logger.error(f'{team_name} is not exists returning {HTTPStatus.NOT_FOUND}')
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Team not found'})
        # return team info
        logger.info(f'Request completed successfully returning HTTP status code:{HTTPStatus.OK.value}')
        return team_info, HTTPStatus.OK.value

    @api.doc(description="Update team information",security='apikey')
    @api.param('Description', 'New Team Description')
    @api.response(HTTPStatus.OK.value, HTTPStatus.OK.phrase, Team.team_info)
    @api.response(HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.phrase)
    @api.response(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.phrase)
    @api.response(HTTPStatus.UNAUTHORIZED.value, HTTPStatus.UNAUTHORIZED.phrase)
    @Authentication.token_required
    def patch(orgnization_ID,self, team_name):
        logger.info(f'PATCH /team/{team_name}')
        # check if team is exists
        is_exists, team_info = Team.is_exists(orgnization_ID, team_name)
        if not is_exists:
            logger.error(f'{team_name} is not exists returning {HTTPStatus.NOT_FOUND}')
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Team not found'})
        # get the new description
        if request.args.get("Description"):
            team_info['Description'] = request.args.get("Description")
        else:
            logger.error(f'No description provided returning {HTTPStatus.BAD_REQUEST}')
            abort(HTTPStatus.BAD_REQUEST.value, {'error':'Description is required'})
        # update team info
        Team.update(orgnization_ID, team_name, team_info)
        # return team info
        logger.info('Request completed successfully returning HTTP status code:{HTTPStatus.OK.value}')
        return team_info, HTTPStatus.OK.value
    
    @api.doc(description="Delete team",security='apikey')
    @api.response(HTTPStatus.OK.value, HTTPStatus.OK.phrase)
    @api.response(HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.phrase)
    @api.response(HTTPStatus.UNAUTHORIZED.value, HTTPStatus.UNAUTHORIZED.phrase)
    @Authentication.token_required
    def delete(organization_ID,self, team_name):
        logger.info(f'DELETE /team/{team_name}')
        # check if the team is exists
        if not Team.is_exists(organization_ID, team_name)[0]:
            logger.error(f'{team_name} is not exists returning {HTTPStatus.NOT_FOUND}')
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Team not found'})
        # delete team
        Team.delete(organization_ID, team_name)
        logger.info('Request completed successfully returning HTTP status code:{HTTPStatus.OK.value}')
        return 'Team Deleted', HTTPStatus.OK.value


@api.route('/<string:team_name>/employees')
class TeamEmployee(Resource):
    @api.doc(description="Get all employees in the team",security='apikey')
    @api.response(HTTPStatus.OK.value , HTTPStatus.OK.phrase  , [Employee.employee_info])
    @api.response(HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.phrase)
    @api.response(HTTPStatus.UNAUTHORIZED.value, HTTPStatus.UNAUTHORIZED.phrase)
    @Authentication.token_required
    def get(organization_id,self, team_name):
        logger.info(f'GET /team/{team_name}/employees')
        # check if team is exists
        if Team.is_exists(organization_id, team_name)[0] == False:
            logger.error(f'{team_name} is not exists returning {HTTPStatus.NOT_FOUND}')
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Team not found'})
        # get all employees in the team
        logger.info(f'Request completed successfully returning HTTP status code:{HTTPStatus.OK.value}')
        return Team.get_employees(organization_id, team_name), HTTPStatus.OK.value

    @api.doc(description="Add employee to the team",security='apikey')
    @api.param('employee_id', 'Employee ID', strict=True)
    @api.response(HTTPStatus.OK.value, HTTPStatus.OK.phrase)
    @api.response(HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.phrase)
    @api.response(HTTPStatus.CONFLICT.value, HTTPStatus.CONFLICT.phrase)
    @api.response(HTTPStatus.UNAUTHORIZED.value, HTTPStatus.UNAUTHORIZED.phrase)
    @Authentication.token_required
    def post(organization_id,self, team_name):
        logger.info(f'POST /team/{team_name}/employees')
        # get employee ID
        employee_id = request.args.get("employee_id")
        # check employee id
        if employee_id == None:
            logger.error(f'No employee ID provided returning {HTTPStatus.BAD_REQUEST}')
            abort(HTTPStatus.BAD_REQUEST.value, {'error':'employee_id is required'})
        # check if the team is exists
        if not Team.is_exists(organization_id, team_name)[0]:
            logger.error(f'{team_name} is not exists returning {HTTPStatus.NOT_FOUND}')
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Team not found'})
        # check if employee is exists
        validate_employee, employee_info = Employee.is_exists(
            organization_id, employee_id)
        if not validate_employee:
            logger.error(f'{employee_id} is not exists returning {HTTPStatus.NOT_FOUND}')
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Employee not found'})
        # check if employee is already in the team
        if Employee.is_in_team(organization_id, employee_id):
            logger.error(f'{employee_id} is already in the team returning {HTTPStatus.CONFLICT}')
            abort(HTTPStatus.CONFLICT.value, {'error':'Employee is already in the team'})
        # add employee to the team
        Employee.add_to_team(organization_id, employee_id, team_name)
        logger.info('Request completed successfully returning HTTP status code:{HTTPStatus.OK.value}')
        return 'Employee added to the team', HTTPStatus.OK.value

    @api.doc(description="Remove employee from the team",security='apikey')
    @api.param('employee_id', 'Employee ID', strict=True)
    @api.response(HTTPStatus.OK.value, HTTPStatus.OK.phrase, Employee.employee_info)
    @api.response(HTTPStatus.NOT_FOUND.value, HTTPStatus.NOT_FOUND.phrase)
    @api.response(HTTPStatus.CONFLICT.value, HTTPStatus.CONFLICT.phrase)
    @api.response(HTTPStatus.BAD_REQUEST.value, HTTPStatus.BAD_REQUEST.phrase)
    @api.response(HTTPStatus.UNAUTHORIZED.value, HTTPStatus.UNAUTHORIZED.phrase)
    @Authentication.token_required
    def delete(organization_id,self, team_name):
        logger.info(f'DELETE /team/{team_name}/employees')
        # get employee ID
        employee_id = request.args.get("employee_id")
        # check employee id
        if employee_id == None:
            logger.error(f'No employee ID provided returning {HTTPStatus.BAD_REQUEST}')
            abort(HTTPStatus.BAD_REQUEST.value, {'error':'employee_id is required'})
        # check if the team is exists
        if not Team.is_exists(organization_id, team_name)[0]:
            logger.error(f'{team_name} is not exists returning {HTTPStatus.NOT_FOUND}')
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Team not found'})
        # check if employee is exists
        validate_employee, employee_info = Employee.is_exists(
            organization_id, employee_id)
        if not validate_employee:
            logger.error(f'{employee_id} is not exists returning {HTTPStatus.NOT_FOUND}')
            abort(HTTPStatus.NOT_FOUND.value, {'error':'Employee not found'})
        # check if employee is in the team
        try:
            if employee_info['TeamID'] != team_name:
                logger.error(f'{employee_id} is not in team returning {HTTPStatus.CONFLICT}')
                abort(HTTPStatus.CONFLICT.value, {'error':'Employee is not in  team'})
        except KeyError:
            logger.error(f'{employee_id} is not in the team to be deleted from it returning {HTTPStatus.CONFLICT}')
            abort(HTTPStatus.CONFLICT.value, {'error':'Employee is not in the team'})
        # remove employee from the team
        employee_info['TeamID'] = None
        # update employee in the database
        Employee.update(organization_id, employee_id, employee_info)
        logger.info(f'Request completed successfully returning HTTP status code:{HTTPStatus.OK.value}')
        return employee_info, HTTPStatus.OK.value
