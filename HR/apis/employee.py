from flask_restx import  Namespace, Resource
from HR.models import employee_model
from HR import db

api = Namespace('Employee', description='Employee related APIs')

@api.route('/')
class EmployeeInfo(Resource):
    def get(self):
        return ''