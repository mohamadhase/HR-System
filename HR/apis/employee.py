# external imports
from flask_restx import Namespace, Resource
from flask import request

# internal imports
from HR import db
from HR.models import employee_add_model
api = Namespace('Employee', description='Employee related APIs')


@api.route('/<string:employee_id>')
class EmployeeInfo(Resource):
    @api.doc(description="Get Spisific  employee information")
    def get(self, employee_id):
        organization_id = 'n0sy1NF8qUHyy46b1gI9'
        employee_ref = db.collection('organization').document(
            organization_id).collection('Employees').document(employee_id)
        if employee_ref.get().exists:
            return employee_ref.get().to_dict(), 200
        return {'message': 'Employee not found'}, 404

    @api.doc(description="Update employee information")
    @api.param('employee_name', 'Employee Name')
    @api.param('employee_email', 'Employee Email')
    @api.param('employee_phone', 'Employee Phone')
    @api.param('employee_address', 'Employee Address')
    @api.param('employee_team_id', 'Employee TeamID')
    def put(self, employee_id):
        organization_id = 'n0sy1NF8qUHyy46b1gI9'
        employee_ref = db.collection('organization').document(
            organization_id).collection('Employees').document(employee_id)
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
    def delete(self, employee_id):
        organization_id = 'n0sy1NF8qUHyy46b1gI9'
        employee_ref = db.collection('organization').document(
            organization_id).collection('Employees').document(employee_id)
        if employee_ref.get().exists:
            employee_ref.delete()
            return {'message': 'Employee deleted successfully'}, 200
        return {'message': 'Employee not found'}, 404

    @api.doc(description="Delete employee", params={'employee_id': 'Employee ID'})
    def delete(self, employee_id):
        organization_id = 'n0sy1NF8qUHyy46b1gI9'
        employee_ref = db.collection('organization').document(
            organization_id).collection('Employees').document(employee_id)
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
        employees_ref = db.collection('organization').document(
            organization_id).collection('Employees')
        if employees_ref.document(employee_info['ID']).get().exists:
            return {'message': 'Employee already exists'}, 400
        team_id = None
        try:
            team_id = employee_info['TeamID']
        except KeyError:
            employee_info['TeamID'] = None
        team_ref = db.collection('organization').document(
            organization_id).collection('Teams').document(team_id)
        if not team_ref.get().exists:
            return {'message': 'Team not found'}, 404

        employees_ref.document(employee_info['ID']).set(employee_info)
        return 'Employee created successfully', 200
