from flask_restx import  Namespace, Resource
api = Namespace('Organization', description='Organization related API')
from HR.models import organization_model

@api.route('/')
class OrganizationInfo(Resource):
    def get(self):
        return ''