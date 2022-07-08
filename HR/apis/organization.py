from flask_restx import  Namespace, Resource
api = Namespace('Organization', description='Organization related API')

@api.route('/')
class OrganizationInfo(Resource):
    def get(self):
        return ''