# external imports
import datetime
from email.policy import HTTP
from functools import wraps
from http import HTTPStatus
from typing import Tuple
from flask import abort, request
from flask_restx import fields
from os import getenv
import requests
# internal imports
from HR import db
from HR import api
from HR.models.Logger import create_logger
logger = create_logger(__name__)
class Bot:
    @staticmethod
    def get_org_id_by_slack_id(orgslackid):
        """get the organization id from the database using the org_slack_id
        
        Args:
            orgslackid (str): the organization slack id to search
        
        Returns:
            str: the organization id
        """
        #get the organization  from the database using the org_slack_id
        org_ref = db.collection('Organization').where('SlackID', '==', orgslackid).get()
        # return the organization id
        return org_ref[0].id
    
    
    def admin_required(f):
        """ decorator to check if the command from admin or not"""
        @wraps(f)
        def decorated(*args, **kwargs):
            user_info = Bot.slack_request(f'users.info?user={request.form["user_id"]}', 'GET')['user']
            #check if the user is admin or not
            if not user_info['is_admin'] :
                blocks = [Bot.create_section('You are not an admin')]
                return {'blocks': blocks}
            return f(*args, **kwargs)

        return decorated

    
    def slack_request(endpoint, method, data=None):
        """make a slack request
        
        Args:
            endpoint (str): the slack endpoint to make the request
            method (str): the method to make the request
            data (dict, optional): the data to send to the slack endpoint. Defaults to None.
        
        Returns:
            dict: the response from the slack endpoint
        """
        # get the slack token from the environment variable
        slack_token = getenv('SLACK_APP_TOKEN')
        # make the slack request
        response = requests.request(method, 'https://slack.com/api/'+endpoint
                                    , data=data, headers={'Authorization': 'Bearer ' + slack_token})
        # return the response
        return response.json()
    
    def create_section(text:str)->dict:
        return {"type": "section","text": {"type": "mrkdwn","text": f"*{text}*"}}
    def create_divider():
        return 		{
			"type": "divider"
		}