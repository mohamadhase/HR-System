# external imports
from flask import Flask
from flask_restx import Api
from firebase_admin import credentials, firestore, initialize_app

# internal imports
from HR.apis.team import api as team_api
from HR.apis.employee_attendance import api as employee_attendance_api
from HR.apis.employee import api as employee_api
from HR.apis.organization import api as organization_api

app = Flask(__name__)
api = Api(app, version='1.0', title='HR Mangement  API',
          description='HR Mangement API')
cred = credentials.Certificate(
    'HR/training2-project-firebase-adminsdk-wc6zh-34db789fab.json')
defult_app = initialize_app(cred)
db = firestore.client()
api.add_namespace(organization_api, path='/organization')
api.add_namespace(employee_api, path='/employee')
api.add_namespace(employee_attendance_api, path='/employee')
api.add_namespace(team_api, path='/team')
