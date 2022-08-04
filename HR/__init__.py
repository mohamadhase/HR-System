# external imports
from flask import Flask
from flask_restx import Api
from firebase_admin import credentials, firestore, initialize_app
from dotenv import load_dotenv
from os import getenv
import logging
import slack
from slackeventsapi import SlackEventAdapter 
from flask_cors import CORS
#internal imports
from HR.models.Logger import *
# create logger 
logger = create_logger(__name__)
#Create a Flask application
app = Flask(__name__)
CORS(app)
logger.info('Flask application created')
#Delete the default Flask 404 error recomindation
app.config['ERROR_404_HELP'] = False
#Load the .env file
load_dotenv()
#get the Secret Key from the .env file
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
#Initialize the authrization for the Swagger docs
authorization = {'apikey': {'type': 'apiKey','in': 'header','name': 'x-acess-token',}}
#Initialize the flask-restx API
api = Api(app, version='1.0', title='HR Mangement  API',description='HR Mangement API',authorizations=authorization)
#certificate for the firebase app
cred = None
try :
    cred = credentials.Certificate(getenv('FIRE_STORE_CRIDENTIALS'))
    logger.info('Firebase credintials initialized')
except Exception as e:
    logger.critical('Firebase app initialization failed')
    logger.exception(e)
    exit()
    
#initialize the firebase app
firebase_app = None
try :
    firebase_app = initialize_app(cred)
    logger.info('Firebase app initialized')
except ValueError as e:
    logger.critical('Firebase app initialization failed')
    logger.exception(e)
    exit()
    
#connect to the firestore database
db = None
try :
    db = firestore.client()
    logger.info('Firestore database connected')
except ValueError as e:
    logger.critical('Firestore database connection failed')
    logger.exception(e)
    exit()
    
#initialize the slack client
client = slack.WebClient(token=getenv('SLACK_TOKEN'))
#initialize the slack event adapter
slack_event_adapter = SlackEventAdapter(getenv('SLACK_SINGNING_SECRET'), '/slack/events', app)
# internal imports
from HR.apis.organization import api as organization_api
from HR.apis.employee import api as employee_api
from HR.apis.employee_attendance import api as employee_attendance_api
from HR.apis.team import api as team_api
from HR.apis.authenticatoion import api as authentication_api
from HR.bot.apis.bot import api as bot_api
#Register the namespaces for the swagger UI
api.add_namespace(organization_api, path='/organization')
logger.info('Organization API registered')
api.add_namespace(employee_api, path='/employee')
logger.info('Employee API registered')
api.add_namespace(employee_attendance_api, path='/employee')
logger.info('Employee Attendance API registered')
api.add_namespace(team_api, path='/team')
logger.info('Team API registered')
api.add_namespace(authentication_api, path='/authentication')
logger.info('Authentication API registered')
api.add_namespace(bot_api, path='/bot')
logger.info('Bot API registered')


