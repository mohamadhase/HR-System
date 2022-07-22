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



@slack_event_adapter.on('team_join')
def new_employee(payload): 
    """event handler for new employee joining the workspace """
    # get employee info from the payload
    employee_data = payload['event']['user']
    # get the organization slack ID from the payload
    org_slack_id = payload['api_app_id']
    # get the organization id from the database using the org_slack_id
    org_id = Bot.get_org_id(org_slack_id)
    # get the employee id from the database using the email
    employee_id = Bot.get_emploee_id(org_id, employee_data['profile']['email'])
    if employee_id == None:
        return 'Employee not found in the database'
    # get the current employee data
    validate, db_employee_data = Employee.is_exists(
        orgnization_ID=org_id, employee_ID=employee_id)
    # update the slack_id
    db_employee_data['SlackID'] = employee_data['id']
    # update the user info in the database
    Employee.update(orgnization_ID=org_id, employee_ID=employee_id,
                    employee_info=db_employee_data)
    return 'User Updated'


@api.route('/salary')
@api.doc(False)
class UserSalary(Resource):
    def post(self):
        # get the user id from the payload
        user_slack_id = request.form['user_id']
        #get the organization slack ID from the payload
        org_slack_id = request.form['api_app_id']
        print(request.form)
        #get the organization id from the database using the org_slack_id
        org_id = Bot.get_org_id(org_slack_id)
        # get the Month and Year from the payload
        args = request.form['text'].split(' ')
        # validate the input data
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
        try :
            user_ref = db.collection('Organization').document(
                org_id).collection('Employees').where(
                    'SlackID', '==', user_slack_id).get()[0]
        except IndexError:
            return 'Your are not registered in the system'

        attends = user_ref.reference.collection('Attendance').where(
            'Month', '==', month).where('Year', '==', year).get()
        houre_price = user_ref.to_dict()['HourPrice']
        salary = 0
        number_of_hours = 0
        for attend in attends:
            attend = attend.to_dict()
            number_of_hours += attend['NumberOfHours']
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
    # send the message as direct message to the user
        client.chat_postMessage(
            channel=f'@{user_slack_id}', blocks=msg, type='mrkdwn')
        return 'Salary info sent to the user'

    def get(self):
        return new_employee()


@api.route('/addattendance')
@api.doc(False)
class AddAttendance(Resource):
    def post(payload):
        # get the user id from the payload
        user_id = request.form['user_id']

        # get today date
        date_dict = {}
        date_dict['Day'] = date.today().day
        date_dict['Month'] = date.today().month
        date_dict['Year'] = date.today().year
        date_dict['Date'] = Employee.dict_to_datetime(date_dict)

        # get the data from the payload

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
        # get the actual user id
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
        # get the user id from the payload
        user_id = request.form['user_id']

        # get today date
        date_dict = {}
        date_dict['Day'] = date.today().day
        date_dict['Month'] = date.today().month
        date_dict['Year'] = date.today().year
        date_dict['Date'] = Employee.dict_to_datetime(date_dict)

        # get the actual user id
        user_ref = db.collection('Organization').document(
            'n0sy1NF8qUHyy46b1gI9').collection('Employees').where(
                'SlackID', '==', user_id).get()[0]
        user_id_db = user_ref.to_dict()['ID']
        # check if the user has attend in this day
        if not Employee.is_attend('n0sy1NF8qUHyy46b1gI9', user_id_db, date_dict)[0]:
            return {'text': f'You have not attend in {date_dict["Date"]}'}

        Employee.delete_attend('n0sy1NF8qUHyy46b1gI9', user_id_db, date_dict)
        return {'text': f'Attendance for {date_dict["Date"]} Deleted successfully'}
