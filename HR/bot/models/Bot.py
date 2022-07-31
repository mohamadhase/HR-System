# external imports
import datetime
from email.policy import HTTP
from functools import wraps
from http import HTTPStatus
from typing import Tuple
from flask import abort, request
from flask_restx import fields
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
            #get the organization id from the org slack id
            org_id = Bot.get_org_id_by_slack_id(request.form['team_id'])
            #
            return f(*args, **kwargs)

        return decorated

