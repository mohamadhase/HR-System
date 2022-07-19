# external imports
from flask_restx import fields
# internal imports
from HR import db
from HR import api


class Organization():
    # Organization model for the returned data
    Organization_info = api.model('Organization_info',  {
        "Name": fields.String(required=True, description="Organization Name"),
        "Address": fields.String(required=True, description="Organization Address"),
        "UserName": fields.String(required=True, description="Organization UserName"),
    })

    @staticmethod
    def get_info(orgnization_ID, teams=False, employees=False):
        """get the information of an organization from the database 

        Args:
            orgnization_ID (string): the ID of the organization 
            teams (bool, optional): flag for the teams to be included in the returned object. Defaults to False.
            employees (bool, optional): flag for the teams to be included in the returned object. Defaults to False.

        Returns:
            dict: the organization information 
        """
        org_ref = db.collection('Organization').document(orgnization_ID)
        orgnization_info = org_ref.get().to_dict()
        if teams:
            orgnization_teams_ref = org_ref.collection('Teams').stream()
            orgnization_teams = [team.to_dict()
                                 for team in orgnization_teams_ref]
            orgnization_info['Teams'] = orgnization_teams
        if employees:
            orgnization_employees_ref = org_ref.collection(
                'Employees').stream()
            orgnization_employees = [employee.to_dict()
                                     for employee in orgnization_employees_ref]
            orgnization_info['Employees'] = orgnization_employees
        return orgnization_info

    @staticmethod
    def update(orgnization_ID, orgnization_info):
        """update the information of an organization in the database

        Args:
            orgnization_ID (string): the ID of the organization
            orgnization_info (dict): dictionary with the new information of the organization

        Returns:
            dict:the updated organization information
        """
        org_ref = db.collection('Organization').document(orgnization_ID)
        org_ref.update(orgnization_info)
        return org_ref.get().to_dict()

    @staticmethod
    def is_exists(orgnization_ID):
        """check if an organization exists in the database
        Args:
            orgnization_ID (string): the ID of the organization
        Returns:
            bool: True if the organization exists, False otherwise
        """
        org_ref = db.collection('Organization').document(orgnization_ID)
        return org_ref.get().exists

    @staticmethod
    def get_teams(orgnization_ID):
        """get the teams of an organization from the database

        Args:
            orgnization_ID (string): [description]

        Returns:
            List(dict): List of the teams of the organization
        """
        teams_ref = db.collection('Organization').document(
            orgnization_ID).collection('Teams').stream()
        teams = [team.to_dict() for team in teams_ref]
        return teams
