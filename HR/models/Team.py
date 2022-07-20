# external imports
from typing import Tuple
from flask_restx import fields
# internal imports
from HR import db
from HR import api
from HR.models.Employee import Employee


class Team:
    team_info = api.model('Team',
                          {
                              "Name": fields.String(required=True, description="Team Name"),
                              "Description": fields.String(required=True, description="Team Description")
                          }, strict=True)

    @staticmethod
    def create(orgnization_ID:str, team_info:dict) -> dict:
        """add a new team to the database

        Args:
            orgnization_ID (string): the organization ID to which the team belongs
            team_info (dict): the team information to be added to the database

        Returns:
            dict : the information of the newly created team
        """
        team_ref = db.collection('Organization').document(
            orgnization_ID).collection('Teams').document(team_info['Name'])

        team_ref.set(team_info)
        return team_ref.get().to_dict()

    @staticmethod
    def is_exists(orgnization_ID:str, team_ID:str)-> Tuple[bool, dict]:
        """check if a team exists in the database

        Args:
            orgnization_ID (string): the organization ID to which the team belongs
            team_ID (string): the team ID to be checked

        Returns:
            (bool,dict): (True if the team exists | False otherwise , the team information) 
        """
        team_ref = db.collection('Organization').document(
            orgnization_ID).collection('Teams').document(team_ID)
        return team_ref.get().exists, team_ref.get().to_dict()

    @staticmethod
    def is_valid_name(team_name:str)->bool:
        """check if a team name is valid for the database
        Returns : 
            bool : True if the team name is valid | False otherwise
        """
        return team_name != ''

    @staticmethod
    def update(orgnization_ID:str, team_name:str, team_info:dict)->None:
        """update a team information in the database

        Args:
            orgnization_ID (string): the organization ID to which the team belongs
            team_name (string): the team name to be updated
            team_info (dict): the new team information to be updated
        """
        db.collection('Organization').document(orgnization_ID).collection(
            'Teams').document(team_name).update(team_info)

    @staticmethod
    def get_employees(orgnization_ID:str, team_name:str)->list[dict]:
        """get all the employees in a team
        Args:
            orgnization_ID (string): the organization ID to which the team belongs
            team_name (string): the team name to be checked
        Returns:
            list[dict]: the list of employees in the team
        """
        employees_ref = db.collection('Organization').document(orgnization_ID).collection(
            'Employees').where('TeamID', '==', team_name).stream()
        employees = [employee.to_dict() for employee in employees_ref]
        return employees

    @staticmethod
    def delete(orgnization_ID:str, team_name:str)->None:
        """delete a team from the database
        
        Args:
            orgnization_ID (str): the organization ID to which the team belongs
            team_name (str): the team name to be deleted
        """
        # remove all the employees from the team
        employee_ref = db.collection('Organization').document(
            orgnization_ID).collection('Employees').where('TeamID', '==', team_name)
        for employee in employee_ref.stream():
            db.collection('Organization').document(orgnization_ID).collection(
                'Employees').document(employee.id).update({'TeamID': None})
        # remove the team
        team_ref = db.collection('Organization').document(
            orgnization_ID).collection('Teams').document(team_name)
        team_ref.delete()
