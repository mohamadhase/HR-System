from flask_restx import  Namespace, Resource
api = Namespace('Employee', description='Employee related APIs')
from HR.models import employee_model

@api.route('/')
class EmployeeInfo(Resource):
    def get(self):
        return ''