from flask_restx import  Namespace, Resource
api = Namespace('Team', description='Team related API')
from HR.models import team_model, organization_model
@api.route('/')
class Team(Resource):
    def get(self):
        return ''