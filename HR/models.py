from HR  import api
from flask_restx import fields



organization_model = api.model('Organization', 
{
"Name": fields.String(required=True, description="Organization Name"),
"Address": fields.String(required=True, description="Organization Address"),
}
,strict=True)

team_model = api.model('Team',
{
"Name": fields.String(required=True, description="Team Name"),
"Description": fields.String(required=True, description="Team Description")
},strict=True)


employee_add_model = api.model('Employee',{
"ID": fields.String(required=True, description="Employee ID"),
"Name": fields.String(required=True, description="Employee Name"),
"Email": fields.String(required=True, description="Employee Email"),
"Phone": fields.String(required=True, description="Employee Phone"),
"Addres": fields.String(required=True, description="Employee Address"),
"TeamID": fields.String(required=False, description="Employee TeamID"),
},strict=True)

employee_attend_model = api.model('Employee Attendance',{
"Day": fields.Integer(required=True, description="Attendance Day"),
"Month": fields.Integer(required=True, description="Attendance Date"),
"Year": fields.Integer(required=True, description="Attendance Year"),
"NumberOfHours": fields.Integer(required=True, description="Number of Hours"),
"Bouns": fields.Integer(required=True, description="Bonus")
},strict=True)
delete_employee_attend_model = api.model('Delete Employee Attendance',{
"Day": fields.Integer(required=True, description="Attendance Day"),
"Month": fields.Integer(required=True, description="Attendance Date"),
"Year": fields.Integer(required=True, description="Attendance Year"),
},strict=True)