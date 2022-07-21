# external imports
from flask_restx import Namespace, Resource
from flask import abort, request, Response
from datetime import date
# internal imports
from HR import client
from HR.models.Employee import Employee
from HR.models.Team import Team
from HR import db
from HR import slack_event_adapter
from HR.models.Bot import Bot
from HR.models.Employee import Employee
api = Namespace('Slack Bot', description='Slack bot related APIs')

#Handle new user event from slack
@slack_event_adapter.on('team_join')
def new_employee(payload):
    print(payload)
    #get employee info from the payload
    employee_data = payload['event']['user']
    print(employee_data)
    #get the organization slack ID from the payload
    org_slack_id = payload['api_app_id']
    print(org_slack_id)
    #get the organization id from the database using the org_slack_id
    org_id = Bot.get_org_id(org_slack_id)
    print(org_id)
    #get the employee id from the database using the email
    employee_id = Bot.get_emploee_id(org_id,employee_data['profile']['email'])
    print(employee_id)
    #check if the user is already in the database
    validate,db_employee_data = Bot.is_the_Employee_exists(employee_data['profile']['email'],org_slack_id)
    print(validate)
    print(db_employee_data)
    #if the user exist 
    if validate:
        #update the slack_id
        db_employee_data['SlackID'] = employee_data['id']
        print(db_employee_data)
        #update the user info in the database
        Employee.update(orgnization_ID=org_id,employee_ID=employee_id,data=db_employee_data)
        return 'User Updated'
    else :
        return 'User not found in the database'

        




@api.route('/salary')
@api.doc(False)
class UserSalary(Resource):
    
    def post(payload):
        # get the user id from the payload
        user_id = request.form['user_id']
        # get the Month and Year from the payload
        args = request.form['text'].split(' ')
        # validate the input data
        print(args)
        if len(args) > 2 or args[0] == '':
            return {'text': 'enter the month and year in the format "month year" Only'}

        try:
            month = int(args[0])
            if month < 1 or month > 12:
                raise ValueError
        except IndexError:
            return {'text': 'Month and Year are required'}
        except ValueError:
            return {'text': 'Month Must be Between 1 and 12'}
        try:
            year = int(args[1])
        except IndexError:
            return {'text': 'Year is required'}

        # get the info from the database
        user_ref = db.collection('Organization').document(
            'n0sy1NF8qUHyy46b1gI9').collection('Employees').where(
                'SlackID', '==', user_id).get()[0]
            
        attends = user_ref.reference.collection('Attendance').where('Month', '==', month).where('Year', '==', year).get()
        houre_price = user_ref.to_dict()['HourPrice']
        salary = 0
        number_of_hours = 0
        for attend in attends:
            attend = attend.to_dict()
            number_of_hours+=attend['NumberOfHours']
        print(number_of_hours*houre_price)
        msg = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"Your salary for {month}/{year} is *{number_of_hours*houre_price}$*"
			}
		},
  		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"you have worked * {number_of_hours} hours *"
			}
		},
      		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"the price per hour is *{houre_price}$ *"
			}
		}
	]
    #send the message as direct message to the user
        client.chat_postMessage(channel=f'@{user_id}',blocks=msg,type='mrkdwn')
        return 'Salary info sent to the user'
    
    def get(self):
        payload = {'token': 'XAZjx2f5pXCUpOxeQ4GHSaSV', 'team_id': 'T03MBGDG50W', 'api_app_id': 'A03PQB033S9', 'event': {'type': 'team_join', 'user': {'id': 'U03Q8B3730W', 'team_id': 'T03MBGDG50W', 'name': 'mn7670313', 'deleted': False, 'color': '99a949', 'real_name': 'mohamad nasser', 'tz': 'Asia/Gaza', 'tz_label': 'Eastern European Summer Time', 'tz_offset': 
10800, 'profile': {'title': '', 'phone': '', 'skype': '', 'real_name': 'mohamad nasser', 'real_name_normalized': 'mohamad nasser', 'display_name': 'mohamad nasser', 'display_name_normalized': 'mohamad nasser', 'fields': {}, 'status_text': '', 'status_emoji': '', 'status_emoji_display_info': [], 'status_expiration': 0, 'avatar_hash': 'g967da46f73a', 'email': 'mn76703d13@gmail.com', 'first_name': 'mohamad', 'last_name': 'nasser', 'image_24': 'https://secure.gravatar.com/avatar/967da46f73a0fb56a8bbc897dcf60682.jpg?s=24&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0001-24.png', 'image_32': 'https://secure.gravatar.com/avatar/967da46f73a0fb56a8bbc897dcf60682.jpg?s=32&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0001-32.png', 'image_48': 'https://secure.gravatar.com/avatar/967da46f73a0fb56a8bbc897dcf60682.jpg?s=48&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0001-48.png', 'image_72': 'https://secure.gravatar.com/avatar/967da46f73a0fb56a8bbc897dcf60682.jpg?s=72&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0001-72.png', 'image_192': 'https://secure.gravatar.com/avatar/967da46f73a0fb56a8bbc897dcf60682.jpg?s=192&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0001-192.png', 'image_512': 'https://secure.gravatar.com/avatar/967da46f73a0fb56a8bbc897dcf60682.jpg?s=512&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0001-512.png', 'status_text_canonical': '', 'team': 'T03MBGDG50W'}, 'is_admin': False, 'is_owner': False, 'is_primary_owner': False, 'is_restricted': False, 'is_ultra_restricted': False, 'is_bot': False, 'is_app_user': False, 'updated': 1658406487, 'is_email_confirmed': True, 'who_can_share_contact_card': 'EVERYONE', 'presence': 'away'}, 'cache_ts': 1658406487, 'event_ts': '1658406487.011200'}, 'type': 'event_callback', 'event_id': 'Ev03QET5QTA7', 'event_time': 1658406487, 'authorizations': [{'enterprise_id': None, 'team_id': 'T03MBGDG50W', 'user_id': 'U03PLM919FG', 'is_bot': True, 'is_enterprise_install': False}], 'is_ext_shared_channel': False}
        print(payload)
        #get employee info from the payload
        employee_data = payload['event']['user']
        print(employee_data)
        #get the organization slack ID from the payload
        org_slack_id = payload['api_app_id']
        print(org_slack_id)
        #get the organization id from the database using the org_slack_id
        org_id = Bot.get_org_id(org_slack_id)
        print(org_id)
        #get the employee id from the database using the email
        employee_id = Bot.get_emploee_id(org_id,employee_data['profile']['email'])
        if employee_id == None:
            return 'Employee not found'
        #check if the user is already in the database
        validate,db_employee_data = Bot.is_the_Employee_exists(employee_data['profile']['email'],org_slack_id)
        print(validate)
        print(db_employee_data)
        #if the user exist 
        if validate:
            #update the slack_id
            db_employee_data['SlackID'] = employee_data['id']
            print(db_employee_data)
            #update the user info in the database
            Employee.update(orgnization_ID=org_id,employee_ID=employee_id,employee_info=db_employee_data)
            return 'User Updated'
        else :
            return 'User not found in the database'

        
@api.route('/addattendance')
@api.doc(False)
class AddAttendance(Resource):
    def post(payload):
        #get the user id from the payload
        user_id = request.form['user_id']
        
        #get today date
        date_dict = {}
        date_dict['Day'] = date.today().day
        date_dict['Month'] = date.today().month
        date_dict['Year'] = date.today().year
        date_dict['Date'] = Employee.dict_to_datetime(date_dict)

        
        #get the data from the payload
        
        data = request.form['text'].split(' ')
        if len(data) > 1 or data[0] == '':
            return {'text': 'Number of hours is required'}
        number_of_hours = 0
        try: 
            number_of_hours = int(data[0])
        except IndexError:
            return {'text': 'Number of hours is required'}
        except ValueError:
            return {'text': 'Number of hours must be a number'}
        #get the actual user id 
        user_ref = db.collection('Organization').document(
            'n0sy1NF8qUHyy46b1gI9').collection('Employees').where(
                'SlackID', '==', user_id).get()[0]
        user_id_db = user_ref.to_dict()['ID']
        date_dict['NumberOfHours'] = number_of_hours
        Employee.add_attend_day('n0sy1NF8qUHyy46b1gI9', user_id_db, date_dict)
        return {'text': f'Attendance for {date_dict["Date"]} added successfully'}

        
        

@api.route('/removeattendance')
@api.doc(False)
class RemoveAttendance(Resource):
    def post(payload):
        #get the user id from the payload
        user_id = request.form['user_id']
        
        #get today date
        date_dict = {}
        date_dict['Day'] = date.today().day
        date_dict['Month'] = date.today().month
        date_dict['Year'] = date.today().year
        date_dict['Date'] = Employee.dict_to_datetime(date_dict)
        
        
        #get the actual user id 
        user_ref = db.collection('Organization').document(
            'n0sy1NF8qUHyy46b1gI9').collection('Employees').where(
                'SlackID', '==', user_id).get()[0]
        user_id_db = user_ref.to_dict()['ID']
        #check if the user has attend in this day
        if not Employee.is_attend('n0sy1NF8qUHyy46b1gI9', user_id_db, date_dict)[0]:
            return {'text': f'You have not attend in {date_dict["Date"]}'}
            
        Employee.delete_attend('n0sy1NF8qUHyy46b1gI9', user_id_db, date_dict)
        return {'text': f'Attendance for {date_dict["Date"]} Deleted successfully'}