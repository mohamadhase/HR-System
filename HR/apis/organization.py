from flask_restx import  Namespace, Resource
from HR.models import organization_model
from HR import db

api = Namespace('Organization', description='Organization related API')

@api.route('/info')
class OrganizationInfo(Resource):
    @api.doc(description='Get  inforamtion about the  Organization')
    @api.response(200, 'Information about the Organization')
    def get(self):
        orgnization_ID = 'n0sy1NF8qUHyy46b1gI9'
        orgnization_info =  db.collection('organization').document(orgnization_ID).get().to_dict()
        return orgnization_info

    @api.doc(description='Update the Organization')
    @api.expect(organization_model, validate=True)
    def put(self):
        orgnization_ID = 'n0sy1NF8qUHyy46b1gI9'
        print(organization_model)
        orgnization_new_info = api.payload
        db.collection('organization').document(orgnization_ID).set(orgnization_new_info)
        return orgnization_new_info
@api.route('/teams')
class OrganizationTeam(Resource):
    @api.doc(description='Get all teams in the Organization')
    def get(self):
        orgnization_ID = 'n0sy1NF8qUHyy46b1gI9'
        teams_ref = db.collection('organization').document(orgnization_ID).get().to_dict()['Teams']
        teams = []
        for index,team in enumerate(teams_ref):
            team['ID'] = index
            teams.append(team)
        return teams
            
     