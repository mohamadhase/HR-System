# external imports
from typing import Tuple
from flask_restx import fields
# internal imports
from HR import db
from HR import api
from HR.models.Logger import *
logger = create_logger(__name__)
class Organization():
    # Organization model for the returned data
    Organization_info = api.model('Organization_info',  {
        "Name": fields.String(required=True, description="Organization Name"),
        "Address": fields.String(required=True, description="Organization Address"),
        "UserName": fields.String(required=True, description="Organization UserName"),
    })

    @staticmethod
    def get_info(orgnization_ID:str, teams=False, employees=False)->dict:
        logger.info(f'getting organization {orgnization_ID} information')
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
        logger.info(f'organization {orgnization_ID} information retrieved successfully')
        return orgnization_info

    @staticmethod
    def update(orgnization_ID:str, orgnization_info:dict)->dict:
        """update the information of an organization in the database

        Args:
            orgnization_ID (string): the ID of the organization
            orgnization_info (dict): dictionary with the new information of the organization

        Returns:
            dict:the updated organization information
        """
        logger.info(f'updating organization {orgnization_ID} information')
        org_ref = db.collection('Organization').document(orgnization_ID)
        org_ref.update(orgnization_info)
        logger.info(f'organization {orgnization_ID} information updated successfully')
        return org_ref.get().to_dict()

    @staticmethod
    def is_exists(orgnization_ID:str)->bool:
        """check if an organization exists in the database
        Args:
            orgnization_ID (string): the ID of the organization
        Returns:
            bool: True if the organization exists, False otherwise
        """
        logger.info(f'checking if organization {orgnization_ID} exists')
        org_ref = db.collection('Organization').document(orgnization_ID)
        return org_ref.get().exists

    @staticmethod
    def get_teams(orgnization_ID:str):
        """get the teams of an organization from the database

        Args:
            orgnization_ID (string): [description]

        Returns:
            List(dict): List of the teams of the organization
        """
        logger.info(f'getting organization {orgnization_ID} teams')
        teams_ref = db.collection('Organization').document(
            orgnization_ID).collection('Teams').stream()
        teams = [team.to_dict() for team in teams_ref]
        logger.info(f'organization {orgnization_ID} teams retrieved successfully')
        return teams
    def get_employees(orgnization_ID:str,team_ID:str=None):
        """get the employees of an organization from the database 
            if the team is given get the employees of the team

        Args:
            orgnization_ID (string): the ID of the organization to get from
            team_ID (string): if its given get the employees of the team
            

        Returns:
            List(dict): List of the employees of the organization or team
        """
        logger.info(f'getting organization {orgnization_ID} employees')
        employees_ref = db.collection('Organization').document(
            orgnization_ID).collection('Employees').stream()
        if team_ID is None:
            employees = [employee.to_dict() for employee in employees_ref]
        else : 
            employees = [employee.to_dict() for employee in employees_ref if employee.to_dict()['TeamID'] == team_ID]

        logger.info(f'organization {orgnization_ID} employees retrieved successfully' )
        return employees