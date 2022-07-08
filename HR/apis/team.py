from flask_restx import  Namespace, Resource
from HR.models import team_model, organization_model
from HR import db



api = Namespace('Team', description='Team related API')
@api.route('/')
class Team(Resource):
    def get(self):
        return ''