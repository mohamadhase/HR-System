from flask_restx import  Namespace, Resource
from pyrsistent import v
from HR.models import employee_add_model,employee_attend_model , delete_employee_attend_model
from HR import db
from flask import request
from HR.functions import *
api = Namespace('Employee', description='Employee related APIs')

@api.route('/<string:employee_id>')
class EmployeeInfo(Resource):
    @api.doc(description="Get Spisific  employee information")
    def get(self,employee_id):
        organization_id = 'n0sy1NF8qUHyy46b1gI9'
        employee_ref = db.collection('organization').document(organization_id).collection('Employees').document(employee_id)
        if employee_ref.get().exists:
            return employee_ref.get().to_dict(), 200
        return {'message': 'Employee not found'}, 404

    
    @api.doc(description="Update employee information")
    @api.param('employee_name', 'Employee Name')
    @api.param('employee_email', 'Employee Email')
    @api.param('employee_phone', 'Employee Phone')
    @api.param('employee_address', 'Employee Address')
    @api.param('employee_team_id', 'Employee TeamID')
    def put(self,employee_id):
        organization_id = 'n0sy1NF8qUHyy46b1gI9'
        employee_ref = db.collection('organization').document(organization_id).collection('Employees').document(employee_id)
        if not employee_ref.get().exists:
            return {'message': 'Employee not found'}, 404
        
        employee_info = employee_ref.get().to_dict()
        if request.args.get('employee_name'):
            employee_info['Name'] = request.args.get('employee_name')
        if request.args.get('employee_email'):
            employee_info['Email'] = request.args.get('employee_email')
        if request.args.get('employee_phone'):
            employee_info['Phone'] = request.args.get('employee_phone')
        if request.args.get('employee_address'):
            employee_info['Address'] = request.args.get('employee_address')
        if request.args.get('employee_team_id'):
            if db.collection('organization').document(organization_id).collection('Teams')\
                .document(request.args.get('employee_team_id')).get().exists:
                employee_info['TeamID'] = request.args.get('employee_team_id')
            else:
                return {'message': 'Team not found'}, 404
        employee_ref.set(employee_info)
        return {'message': 'Employee updated successfully'}, 200
    
    @api.doc(description="Delete employee information")
    def delete(self,employee_id):
        organization_id = 'n0sy1NF8qUHyy46b1gI9'
        employee_ref = db.collection('organization').document(organization_id).collection('Employees').document(employee_id)
        if employee_ref.get().exists:
            employee_ref.delete()
            return {'message': 'Employee deleted successfully'}, 200
        return {'message': 'Employee not found'}, 404




    
    @api.doc(description="Delete employee",params={'employee_id':'Employee ID'})
    def delete(self,employee_id):
        organization_id = 'n0sy1NF8qUHyy46b1gI9'
        employee_ref = db.collection('organization').document(organization_id).collection('Employees').document(employee_id)
        if employee_ref.get().exists:
            employee_ref.delete()
            return {'message': 'Employee deleted'}, 200
        return {'message': 'Employee not found'}, 404

@api.route('/')
class Employee(Resource):
    @api.doc(description="Create new employee")
    @api.expect(employee_add_model, validate=True) 
    def post(self):
        organization_id = 'n0sy1NF8qUHyy46b1gI9'
        employee_info = api.payload
        employees_ref = db.collection('organization').document(organization_id).collection('Employees')
        if employees_ref.document(employee_info['ID']).get().exists:
            return {'message': 'Employee already exists'}, 400
        team_id  = None
        try : 
            team_id = employee_info['TeamID']
        except KeyError :
            employee_info['TeamID'] = None
        team_ref = db.collection('organization').document(organization_id).collection('Teams').document(team_id)
        if not team_ref.get().exists:
            return {'message': 'Team not found'}, 404
        
        employees_ref.document(employee_info['ID']).set(employee_info)
        return 'Employee created successfully', 200

@api.route('/<string:employee_id>/attendance')
class EmployeeAttendance(Resource):
    @api.doc(description="Get Spisific  employee attendance")
    @api.param('day', 'Day of the month')
    @api.param('month', 'Month of the year')
    @api.param('year', 'Year')
    def get(self,employee_id):
        organization_id = 'n0sy1NF8qUHyy46b1gI9'
        attend_date = {}
        if not request.args.get('day'):
            return {'message': 'Day not found'}, 404
        if not request.args.get('month'):
            return {'message': 'Month not found'}, 404
        if not request.args.get('year'):
            return {'message': 'Year not found'}, 404
        attend_date['Day'] = int(request.args.get('day'))
        attend_date['Month'] = int(request.args.get('month'))
        attend_date['Year'] = int(request.args.get('year'))
        validate_date = check_date(attend_date)
        if validate_date !=True:
            return {'message': validate_date}, 400
        date = dict_to_datetime(attend_date)
        employee_attends_ref = db.collection('organization').document(organization_id).collection('Employees').document(employee_id).collection('Attendance')
        
        if employee_attends_ref.document(date).get().exists:
            return employee_attends_ref.document(date).get().to_dict(), 200
        return {'message': 'Attendance not found'}, 404




    
    @api.doc(description="Update employee attendance")
    @api.param('day', 'Day of the month',required=True)
    @api.param('month', 'Month of the year',required=True)
    @api.param('year', 'Year',required=True)
    @api.param('number_of_hours', 'Number of hours',required=True)

    def put(self,employee_id):
        #check if the employee exits

        organization_id = 'n0sy1NF8qUHyy46b1gI9'
        attend_date = {}
        if not request.args.get('day'):
            return {'message': 'Day not found'}, 404
        if not request.args.get('month'):
            return {'message': 'Month not found'}, 404
        if not request.args.get('year'):
            return {'message': 'Year not found'}, 404
        if not request.args.get('number_of_hours'):
            return {'message': 'Number of hours not found'}, 404
        attend_date['Day'] = int(request.args.get('day'))
        attend_date['Month'] = int(request.args.get('month'))
        attend_date['Year'] = int(request.args.get('year'))
        attend_date['NumberOfHours'] = int(request.args.get('number_of_hours'))
        validate_date = check_date(attend_date)
        if validate_date !=True:
            return {'message': validate_date}, 400
        date = dict_to_datetime(attend_date)
        employee_attends_ref = db.collection('organization').document(organization_id).collection('Employees').document(employee_id).collection('Attendance')
        if employee_attends_ref.document(date).get().exists:
            employee_attends_ref.document(date).set(attend_date)
            return {'message': 'Attendance updated successfully'}, 200
        return {'message': 'Attendance not found'}, 404
        



    
    
    @api.doc(description="Delete employee attendance",params={'employee_id':'Employee ID'})
    @api.param('day', 'Day of the month',required=True)
    @api.param('month', 'Month of the year',required=True)
    @api.param('year', 'Year',required=True)
    def delete(self,employee_id):
        #check if the employee exits

        organization_id = 'n0sy1NF8qUHyy46b1gI9'
        attend_date = {}
        if not request.args.get('day'):
            return {'message': 'Day not found'}, 404
        if not request.args.get('month'):
            return {'message': 'Month not found'}, 404
        if not request.args.get('year'):
            return {'message': 'Year not found'}, 404
        attend_date['Day'] = int(request.args.get('day'))
        attend_date['Month'] = int(request.args.get('month'))
        attend_date['Year'] = int(request.args.get('year'))
        validate_date = check_date(attend_date)
        if validate_date !=True:
            return {'message': validate_date}, 400
        date = dict_to_datetime(attend_date)
            
        employee_attends_ref = db.collection('organization').document(organization_id).collection('Employees').document(employee_id).collection('Attendance')
        if employee_attends_ref.document(date).get().exists:
            employee_attends_ref.document(date).delete()
            return {'message': 'Attendance deleted successfully'}, 200
        return {'message': 'Attendance not found'}, 404





    @api.doc(description="Add employee attendance")
    @api.expect(employee_attend_model,validate=True)
    def post(self,employee_id):
        organization_id = 'n0sy1NF8qUHyy46b1gI9'
        attend_info = api.payload
        employee_ref = db.collection('organization').document(organization_id).collection('Employees').document(employee_id)
        if not employee_ref.get().exists:
            return {'message': 'Employee not found'}, 404
        date_validate = check_date(attend_info)
        if attend_info['NumberOfHours'] < 1 and attend_info['NumberOfHours'] > 8:
            return {'message': 'Number of hours must be between 1 and 8'}, 400
        if attend_info['Bouns']<0 or attend_info['Bouns']+ attend_info['NumberOfHours'] > 24:
            return {'message': 'Invalid Bonus hours'}, 400

        if date_validate ==True:
            attend_info['Date'] = dict_to_datetime(attend_info)
            if employee_ref.collection('Attendance').document(attend_info['Date']).get().exists:
                return {'message': 'Employee attendance already exists'}, 400
            print(attend_info)
            attends_ref = db.collection('organization').document(organization_id).collection('Employees').document(employee_id).collection('Attendance')
            attends_ref.document(attend_info['Date']).set(attend_info)
            return {'message': 'Attendance added successfully'}, 200
        else:
            return {'message': date_validate}, 400
           



    