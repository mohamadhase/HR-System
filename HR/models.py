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


employee_model = api.model('Employee',{
"Name": fields.String(required=True, description="Employee Name"),
"Email": fields.String(required=True, description="Employee Email"),
"Phone": fields.String(required=True, description="Employee Phone"),
"Address": fields.String(required=True, description="Employee Address"),
},strict=True)

employee_attend_model = api.model('Employee Attendance',{
"Day": fields.Integer(required=True, description="Attendance Day"),
"Month": fields.Integer(required=True, description="Attendance Date"),
"Year": fields.Integer(required=True, description="Attendance Year"),
"NumberOfHours": fields.Integer(required=True, description="Number of Hours")
},strict=True)
delete_employee_attend_model = api.model('Employee Attendance',{
"Day": fields.Integer(required=True, description="Attendance Day"),
"Month": fields.Integer(required=True, description="Attendance Date"),
"Year": fields.Integer(required=True, description="Attendance Year"),
},strict=True)