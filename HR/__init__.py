# external imports
from pydoc import doc
from flask import Flask
from flask_restx import Api
from firebase_admin import credentials, firestore, initialize_app
from dotenv import load_dotenv
from os import getenv

import slack


#Create a Flask application
app = Flask(__name__)
#connect to slack using the slack token
client  = slack.WebClient(token=getenv('SLACK_APP_TOKEN'))
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
cred = credentials.Certificate(getenv("FIRE_STORE_CRIDENTIALS"))
#initialize the firebase app
defult_app = initialize_app(cred)
#connect to the firestore database
db = firestore.client()
# internal imports
from HR.apis.organization import api as organization_api
from HR.apis.employee import api as employee_api
from HR.apis.employee_attendance import api as employee_attendance_api
from HR.apis.team import api as team_api
from HR.apis.authenticatoion import api as authentication_api
<<<<<<< HEAD
#Register the namespaces for the swagger UI
=======
from HR.apis.bot import api as bot_api
>>>>>>> slackBot
api.add_namespace(organization_api, path='/organization')
api.add_namespace(employee_api, path='/employee')
api.add_namespace(employee_attendance_api, path='/employee')
api.add_namespace(team_api, path='/team')
api.add_namespace(authentication_api, path='/authentication')
api.add_namespace(bot_api, path='/bot')
