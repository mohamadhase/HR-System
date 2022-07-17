# external imports
from pydoc import doc
from flask import Flask
from flask_restx import Api
from firebase_admin import credentials, firestore, initialize_app
import slack
from slackeventsapi import SlackEventAdapter


app = Flask(__name__)
client  = slack.WebClient(token='xoxb-3725557549030-3802723043526-92bxLTmd95GX6kckDu5kJX64')

# slack_event_adapter = SlackEventAdapter('4cac3df81d06265cc593197b73f9e9ad','/slack/events',app)
# @slack_event_adapter.on('message')
# def message(payload):
#     print(payload)

app.config['ERROR_404_HELP'] = False
app.config['SECRET_KEY'] = 'super-secret'
authorization = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'x-acess-token',
    }
}

api = Api(app, version='1.0', title='HR Mangement  API',
          description='HR Mangement API',authorizations=authorization)
cred = credentials.Certificate(
    'HR/training2-project-firebase-adminsdk-wc6zh-34db789fab.json')
defult_app = initialize_app(cred)
db = firestore.client()
# internal imports
from HR.apis.organization import api as organization_api
from HR.apis.employee import api as employee_api
from HR.apis.employee_attendance import api as employee_attendance_api
from HR.apis.team import api as team_api
from HR.apis.authenticatoion import api as authentication_api
from HR.apis.bot import api as bot_api
api.add_namespace(organization_api, path='/organization')
api.add_namespace(employee_api, path='/employee')
api.add_namespace(employee_attendance_api, path='/employee')
api.add_namespace(team_api, path='/team')
api.add_namespace(authentication_api, path='/authentication')
api.add_namespace(bot_api, path='/bot')
