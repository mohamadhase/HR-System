from flask_restx import  Namespace, Resource
api = Namespace('Employee', description='Employee related APIs')

@api.route('/')
class EmployeeInfo(Resource):
    def get(self):
        return ''