# internal imports
from typing import Tuple
from HR import db
from HR import api

class Bot:
    """Class for all the bot related functions"""
    def is_the_Employee_exists(employee_email: str,org_slack_id:str) -> Tuple[bool,dict]:
        """check if the employee is already in the database using the email
        Args:
            employee_email (str): the employee email 
            org_slack_id (str): the organization slack id to search in

        Returns:
            Tuple[bool,dict]: (True,employee_info) if the employee is in the database else (False,None)
        """
        #get the organization  from the database using the org_slack_id
        org_ref = db.collection('Organization').where('SlackID', '==', org_slack_id).get()
        # get the employee from the database using the employee_slack_id
        emp_ref = org_ref[0].reference.collection('Employees').where('Email', '==', employee_email).get()
        
        # if the employee is in the database return True and the employee info else return False and None
        return (emp_ref[0].exists,emp_ref[0].to_dict())


    def get_org_id(org_slack_id:str) -> str:
        """get the organization id from the database using the org_slack_id
        
        Args:
            org_slack_id (str): the organization slack id to search in
        
        Returns:
            str: the organization id
        """
        #get the organization  from the database using the org_slack_id
        org_ref = db.collection('Organization').where('SlackID', '==', org_slack_id).get()
        # return the organization id
        return org_ref[0].id
    def get_emploee_id(org_id:str,email:str) -> str:
        """get the employee id from the database using the employee_slack_id
        
        Args:
            email (str): the employee email to search for
            org_id (str): the organization  id to search in
        
        Returns:
            str: the employee id
        """
        emp_ref = db.collection('Organization').document(org_id).collection('Employees').where('Email', '==', email).get()
        try :
            return emp_ref[0].id
        except IndexError:
            return None