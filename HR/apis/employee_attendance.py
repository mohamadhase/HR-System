from flask_restx import  Namespace, Resource
api = Namespace('Employee Attendance', description='Employee Attendance related APIs')
from HR.models import employee_attendance_model,delete_employee_attend_model

@api.route('/')
class EmployeeAttendance(Resource):
    def get(self):
        return ''