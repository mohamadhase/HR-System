from flask_restx import  Namespace, Resource
from HR.models import employee_attend_model , delete_employee_attend_model
from HR import db

api = Namespace('Employee Attendance', description='Employee Attendance related APIs')

@api.route('/')
class EmployeeAttendance(Resource):
    def get(self):
        return ''