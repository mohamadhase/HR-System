from flask_restx import Namespace, Resource
from flask import abort
from http import HTTPStatus
from flask import request 

# internal imports
from HR import api
from HR.models.Organization import Organization
from HR.models.Employee import Employee
from HR.bot.models.Bot import Bot
from HR.models.Logger import create_logger
from HR import slack_event_adapter
from HR import client
from os import getenv
logger = create_logger(__name__)
api = Namespace('slackBot', description='Slack Bot related APIs')

@slack_event_adapter.on('message')
def message(payload):
    print(payload)


@slack_event_adapter.on('team_join')
def new_employee(payload): 
    """event handler for new employee joining the workspace """
    employee_data = payload['event']['user']        
    #get organization id from the org slack id
    org_id = Bot.get_org_id_by_slack_id(payload['team_id'])
    #create a new employee in the database
    employee_db_data = {}
    employee_db_data['Address'] = ''
    employee_db_data['Email'] = employee_data['profile']['email']
    employee_db_data['HourPrice']= 0
    employee_db_data['ID']= employee_data['id']
    employee_db_data['name']= employee_data['real_name']
    employee_db_data['phone']= employee_data['profile']['phone']
    employee_db_data['SlackID'] = employee_data['id']
    employee_db_data['Team_ID']= None
    Employee.create(org_id,employee_db_data)        
    return {'msg':'Emploee Created Successfully'}


@api.route('/admin/employees')
class AdminEmployees(Resource):
    #@Bot.admin_required
    def post(self):
        #get organization id from the org slack id
        org_id = Bot.get_org_id_by_slack_id(request.form['team_id'])
        print(client.users_info(user=request.form['user_id'],token=getenv('SLACK_APP_TOKEN')))
        
        pass      
        

        
        