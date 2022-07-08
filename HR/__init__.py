from flask import Flask
from flask_restx import Api

app = Flask(__name__)
api = Api(app , version='1.0' , title='HR Mangement  API' , description='HR Mangement API')

from HR.apis.organization import api as organization_api
from HR.apis.employee import api as employee_api
from HR.apis.employee_attendance import api as employee_attendance_api
from HR.apis.team import api as team_api


api.add_namespace(organization_api, path='/organization')

api.add_namespace(employee_api, path='/employee')
api.add_namespace(employee_attendance_api, path='/employee_attendance')
api.add_namespace(team_api, path='/team')