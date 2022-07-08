from flask_restx import  Namespace, Resource
api = Namespace('Team', description='Team related API')
@api.route('/')
class Team(Resource):
    def get(self):
        return ''