from datetime import datetime
from multiprocessing.dummy import Value
from flask_restx import Namespace, Resource
from flask import abort
from http import HTTPStatus
from flask import request
from numpy import block 
from requests.structures import CaseInsensitiveDict
import requests
import calendar

# internal imports
from HR import api
from HR.models.Organization import Organization
from HR.models.Employee import Employee
from HR.models.Team import Team
from HR.bot.models.Bot import Bot
from HR.models.Logger import create_logger
from HR import slack_event_adapter
from HR import client
from os import getenv
logger = create_logger(__name__)
api = Namespace('slackBot', description='Slack Bot related APIs')

@slack_event_adapter.on('message')
def message(payload):
    blocks = []
    
    if payload['event']['text']=='help':
        blocks = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Welcome* to the HR Bot.\n\n"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Admin Commands*"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "1. /userinfo [UserID] e.g /userinfo @mohamadhase  \n *get the information about given user*"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "2. /teams [TeamName] e.g /teams backend  \n * get the information about given team* \n *if the team name not given will return all teams in the org* "
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "3. /attendances [UserID] e.g /attendances @mohamadhase  \n *get is the given user is attended or not * \n  *if the UserID not given will return the list of all attended employees *"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Employee Commands*"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "1. /addattend [NumberOfHours] \n *add me as an attended in this day with the given number of hours*"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "2. /deleteattend  \n *delete my attendance in this day *"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "3./getattend [Day/Month/Year]  \n *get the imformation about attendance in the given date *"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "4. /salary  \n *get the information about the salary in the current month *"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "5. /attendreport[Month] [Year]  \n *get full report about your attendance in the given month *"
			}
		}
	]

        client.chat_postMessage(channel='@'+payload['event']['user'], blocks=blocks ,token=getenv('SLACK_APP_TOKEN'))
        return {'blocks': blocks}  
        
    


@slack_event_adapter.on('team_join')
def new_employee(payload): 
    blocks =[]
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
    employee_db_data['Name']= employee_data['real_name']
    employee_db_data['Phone']= employee_data['profile']['phone']
    employee_db_data['SlackID'] = employee_data['id']
    employee_db_data['TeamID']= None
    Employee.create(org_id,employee_db_data)  
    blocks.append(Bot.create_section('Emploee Created Successfully'))
    blocks.append(Bot.create_divider())     
    return{'blocks':blocks}


@api.route('/admin/employees')
class AdminEmployees(Resource):
    @Bot.admin_required
    def post(self):
        blocks = []
        #get organization id from the org slack id
        org_id = Bot.get_org_id_by_slack_id(request.form['team_id'])
        #get the team_id from the request
        team_id = request.form['text']
        print(team_id)
        #validate if the team_id is valid
        if team_id=='' or team_id==None or team_id==' ':
            employees = Organization.get_employees(org_id)
        else:
            if  not Team.is_exists(org_id,team_id)[0]:
                blocks.append(Bot.create_section('Team does not exist'))
                blocks.append(Bot.create_divider())     

                return {'blocks':blocks}
            else:
                
                employees = Organization.get_employees(org_id,team_id)

        #create a list of slack blocks
    
        for employee in employees:
            print(employee)
            id_section = Bot.create_section(f'ID: {employee["ID"]}')
            name_section = Bot.create_section(f'Name: {employee["Name"]}')
            team_id_section = Bot.create_section(f'Team ID: {employee["TeamID"]}')
            phone_section = Bot.create_section(f'Phone: {employee["Phone"]}')
            email_section = Bot.create_section(f'Email: {employee["Email"]}')
            hour_price = Bot.create_section(f'Hour Price: {employee["HourPrice"]}')
            blocks.append(id_section)
            blocks.append(name_section)
            blocks.append(team_id_section)
            blocks.append(phone_section)
            blocks.append(email_section)
            blocks.append(hour_price)
            blocks.append(Bot.create_divider())
        return {'blocks':blocks}

@api.route('/admin/teams')
class AdminTeams(Resource):
    @Bot.admin_required
    def post(self):
        blocks = []
        #get organization id from the org slack id
        org_id = Bot.get_org_id_by_slack_id(request.form['team_id'])
        #get all teams from the organization
        teams = Organization.get_teams(org_id)
        #check if the user send spicific team_id
        team_id = request.form['text']
        if team_id=='' or team_id==None or team_id==' ':
            pass
        else : 
            for team in teams :
                if team['Name']==team_id:
                    teams = [team]
                    break
            else :
                blocks.append(Bot.create_section('Team does not exist'))
                blocks.append(Bot.create_divider())     

                return {'blocks':blocks}
        #create the message to send to the user
        blocks = []
        for index,teams in enumerate(teams):
            index_section = Bot.create_section(f'Team {index+1}')
            name_section = Bot.create_section(f'Team Name : {teams["Name"]}')
            description_section = Bot.create_section(f'Team Description : {teams["Description"]}')
            blocks.append(index_section)
            blocks.append(name_section)
            blocks.append(description_section)
            blocks.append(Bot.create_divider())
        
        return {'blocks':blocks}
    
@api.route('/admin/user')
class AdminUser(Resource):
    @Bot.admin_required
    def post(self):
        blocks = []
        #get organization id from the org slack id
        org_id = Bot.get_org_id_by_slack_id(request.form['team_id'])
        #get the user_id from the request
        user_id = request.form['text']
        #filter the user id from the text 
        try :
            user_id = user_id[2:user_id.index('|')]
        except Exception:
            blocks.append(Bot.create_section('Invalid User ID'))
            blocks.append(Bot.create_divider())     

            return {'blocks':blocks}
        
        #check if the user is valid
        validate, user_info = Employee.is_exists(org_id,user_id)
        if not validate:
            blocks.append(Bot.create_section('User does not exist'))
            return {'blocks':blocks}
        blocks.append(Bot.create_section(f'ID: {user_info["ID"]}'))
        blocks.append(Bot.create_section(f'Name: {user_info["Name"]}'))
        blocks.append(Bot.create_section(f'Team ID: {user_info["TeamID"]}'))
        blocks.append(Bot.create_section(f'Phone: {user_info["Phone"]}'))
        blocks.append(Bot.create_section(f'Email: {user_info["Email"]}'))
        blocks.append(Bot.create_section(f'Hour Price: {user_info["HourPrice"]}'))
        blocks.append(Bot.create_divider())     

        return {'blocks':blocks}
        
@api.route('/user/attendance/add')
class AddAttendance(Resource):
    def post(self):
        blocks = []
        #get organization id from the org slack id
        org_id = Bot.get_org_id_by_slack_id(request.form['team_id'])
        #get the user_id from the request
        user_id = request.form['user_id']
        #get the number of hours from the request
        number_of_hours = request.form['text']
        #check the validation of the number of hours
        try :
            number_of_hours = int(number_of_hours)
        except ValueError:
            blocks.append(Bot.create_section('Invalid Number of Hours'))
            blocks.append(Bot.create_divider())     

            return {'blocks':blocks}
        #check if the user is exists 
        if not  Employee.is_exists(org_id,user_id)[0]:
            blocks.append(Bot.create_section('User does not exist'))
            blocks.append(Bot.create_divider())     

            return {'blocks':blocks}
        #get the date of today
        today_date = datetime.now()
        date_dict = {'Year':today_date.year,'Month':today_date.month,'Day':today_date.day,'NumberOfHours':number_of_hours,'Date':today_date.strftime('%Y-%m-%d')}
        #check if the user attendance is already exists
        if  Employee.is_attend(org_id,user_id,date_dict)[0]:
            blocks.append(Bot.create_section('User attendance is already exists'))
            blocks.append(Bot.create_divider())     

            return {'blocks':blocks}
        #add the attendance to the database
        Employee.add_attend_day(org_id,user_id,date_dict)
        blocks.append(Bot.create_section('Attendance added successfully'))
        blocks.append(Bot.create_divider())     

        return {'blocks':blocks}
@api.route('/user/attendance/get')
class GetAttend(Resource):
    def post(self):
        blocks = []
        #get organization id from the org slack id
        org_id = Bot.get_org_id_by_slack_id(request.form['team_id'])
        #get the user_id from the request
        user_id = request.form['user_id']
        #check if the user is exists
        if not Employee.is_exists(org_id,user_id)[0]:
            blocks.append(Bot.create_section('User does not exist'))
            blocks.append(Bot.create_divider())     

            return {'blocks':blocks}
        #get the date given by the user
        date = request.form['text']
        try :
            date = datetime.strptime(date,'%d/%m/%Y')
            date = date.strftime('%Y-%m-%d')
        except ValueError:
            blocks.append(Bot.create_section('Invalid Date'))
            blocks.append(Bot.create_divider())     

            return {'blocks':blocks}
        #convert the date to dict format
        date = {'Date':date}
        #get the attendance of the user on the given date
        validate,attendance_info = Employee.is_attend(org_id,user_id,date)
        if not validate:
            blocks.append(Bot.create_section('User attendance is not exists'))
            blocks.append(Bot.create_divider())     

            return {'blocks':blocks}
        blocks.append(Bot.create_section(f'Date: {attendance_info["Date"]}'))
        blocks.append(Bot.create_section(f'NumberOfHours: {attendance_info["NumberOfHours"]}'))
        blocks.append(Bot.create_divider())     

        return {'blocks':blocks}
@api.route('/user/attendance/delete')
class DeleteAttendance(Resource):
    def post(self):
        blocks = []
        #get organization id from the org slack id
        org_id = Bot.get_org_id_by_slack_id(request.form['team_id'])
        #get the user_id from the request
        user_id = request.form['user_id']
        #check if the user is exists
        if not Employee.is_exists(org_id,user_id)[0]:
            blocks.append(Bot.create_section('User does not exist'))
            blocks.append(Bot.create_divider())     

            return {'blocks':blocks}
        #get the date of the attendance to be deleted
        date = datetime.now().strftime('%Y-%m-%d')
        #convert the date to dict format
        date = {'Date':date}
        #check if the attendance is exists in the database
        if not  Employee.is_attend(org_id,user_id,date)[0]:
            blocks.append(Bot.create_section('User attendance is not exists'))
            blocks.append(Bot.create_divider())     
            return {'blocks':blocks}
        #delete the attendance of the user on the given date
        Employee.delete_attend(org_id,user_id,date)
        blocks.append(Bot.create_section('Attendance deleted successfully'))
        blocks.append(Bot.create_divider())     
        return {'blocks':blocks}

@api.route('/user/attendance/report')
class AttendanceReport(Resource):
    def post(self):
        blocks = []
        #get organization id from the org slack id
        org_id = Bot.get_org_id_by_slack_id(request.form['team_id'])
        #get the user_id from the request
        user_id = request.form['user_id']
        #check if the user is exists
        if not Employee.is_exists(org_id,user_id)[0]:
            blocks.append(Bot.create_section('User does not exist'))
            blocks.append(Bot.create_divider())     

            return {'blocks':blocks}
        #get the month and year from the request
        args = request.form['text'].split(' ')
        try :
            month = int(args[0])
            year = int(args[1])
            if month not in range(1,13) and year not in range(1900,2100):
                raise ValueError
        except ValueError:
            blocks.append(Bot.create_section('Invalid Month or Year'))
            blocks.append(Bot.create_divider())     

            return {'blocks':blocks}
        #get all the attendance of the user 
        attends = Employee.get_all_attends(org_id,user_id)
        #filer the attendance of the user on the given month and year
        attends = [attend for attend in attends  if attend['Month'] == month and attend['Year'] == year]
        #create the attendance report for slack
        currentDate = datetime.now()

        daysInMonth= calendar.monthrange(currentDate.year, currentDate.month)[1]
        blocks.append(Bot.create_section(f'Attendance Report for {month}/{year}'))
        blocks.append(Bot.create_section(f'This Month consists of {daysInMonth} days'))
        blocks.append(Bot.create_section(f'You have attended {len(attends)} days'))
        for attend in attends:
            blocks.append(Bot.create_section(f'Date: {attend["Date"]}'))
            blocks.append(Bot.create_section(f'NumberOfHours: {attend["NumberOfHours"]}'))
            blocks.append(Bot.create_divider())     
        blocks.append(Bot.create_section(f'Total Hours: {sum([attend["NumberOfHours"] for attend in attends])}'))
        blocks.append(Bot.create_section(f'Your Attendance Percentage: {(len(attends)/daysInMonth)*100}%'))
        blocks.append(Bot.create_divider())     
        return {'blocks':blocks}        
        
@api.route('/user/salary')
class Salary(Resource):
    def post(self):
        blocks = []
        #get organization id from the org slack id
        org_id = Bot.get_org_id_by_slack_id(request.form['team_id'])
        #get the user_id from the request
        user_id = request.form['user_id']
        #check if the user is exists
        validate, userinfo  = Employee.is_exists(org_id,user_id)
        if not validate:
            blocks.append(Bot.create_section('User does not exist'))
            blocks.append(Bot.create_divider())     

            return {'blocks':blocks}
        #get the hour price for the user
        hour_price =int(userinfo['HourPrice'])
        #get all attends of the user
        attends = Employee.get_all_attends(org_id,user_id)
        #get the current month and year
        month,year = datetime.now().month,datetime.now().year
        #filter the attendance of the user on the given month and year
        attends = [attend for attend in attends if attend['Month'] == month and attend['Year'] == year]
        #get the total number of hours of the user
        number_of_hours = int(sum([attend['NumberOfHours'] for attend in attends]))
        #get the total salary of the user
        salary = number_of_hours * hour_price
        blocks.append(Bot.create_section(f'Your Salary for {month}/{year} is {salary}'))
        blocks.append(Bot.create_section(f'You have attended {number_of_hours} hours'))
        blocks.append(Bot.create_section(f'Your Hour Price is {hour_price}'))
        blocks.append(Bot.create_divider())     

        return {'blocks':blocks}
    
@api.route('/admin/attendance/report')
class AdminAttendance(Resource):
    @Bot.admin_required
    def post(self):        
        blocks = []
        response_url = request.form['response_url']
        #send respose to prevent slack from timing out
        requests.post(response_url, json=200)
        
        #get organization id from the org slack id
        org_id = Bot.get_org_id_by_slack_id(request.form['team_id'])
        #check if the user id is given in the request
        user_id = request.form['text']
        try :
            user_id = user_id[2:user_id.index('|')]
        except Exception:
            user_id = None
        #get the current date as string format in the format of 'YYYY-MM-DD'
        date = {'Date':datetime.now().strftime('%Y-%m-%d')}
        #get all the employees of the organization
        employees = Organization.get_employees(org_id)
        #filter the employees if the user id is given
        if user_id:
            employees = [employee for employee in employees if employee['ID'] == user_id]
        #filter the attendant employees
        employees = [employee for employee in employees if Employee.is_attend(org_id,employee['ID'],date)[0]]

        #create the attendance report for slack
        if user_id :
            if len(employees) == 0:
                blocks.append(Bot.create_section('No The Employee is not present'))
                blocks.append(Bot.create_divider())
                return {'blocks':blocks}
            else :
                blocks.append(Bot.create_section(f'Attendance Report for {date["Date"]}'))
                blocks.append(Bot.create_section(f'The Employee is present'))
                blocks.append(Bot.create_divider())
                return {'blocks':blocks}
        if len(employees) == 0:
            blocks.append(Bot.create_section('NO Employees '))
            blocks.append(Bot.create_divider())
            return {'blocks':blocks}
                
        blocks.append(Bot.create_section(f'Attendance Report for {date["Date"]}'))
        blocks.append(Bot.create_section(f'Total Employees attended: {len(employees)}'))
        for employee in employees:
            blocks.append(Bot.create_section(f'{employee["Name"]}'))
            blocks.append(Bot.create_divider())
           
        return {'blocks':blocks}