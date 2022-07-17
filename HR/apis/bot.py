# external imports
from flask_restx import Namespace, Resource
from flask import abort, request, Response
from datetime import date
# internal imports
from HR import client
from HR.models.Employee import Employee
from HR.models.Team import Team
from HR import db
api = Namespace('Slack Bot', description='Slack bot related APIs')


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
