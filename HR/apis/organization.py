from flask_restx import  Namespace, Resource
from HR.models import organization_model
api = Namespace('Organization', description='Organization related API')
from HR import db

@api.route('/')
class OrganizationInfo(Resource):
    def get(self):
        return ''