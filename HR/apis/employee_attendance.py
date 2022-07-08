from flask_restx import  Namespace, Resource
api = Namespace('Employee Attendance', description='Employee Attendance related APIs')

@api.route('/')
class EmployeeAttendance(Resource):
    def get(self):
        return ''