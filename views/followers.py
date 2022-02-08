from operator import and_
from flask import Response, request
from flask_restful import Resource
from models import Following
import json

from sqlalchemy import and_
from views import get_authorized_user_ids

def get_path():
    return request.host_url + 'api/posts/'

class FollowerListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # Goal: Generate list of user objects representing list of users who are following the current user
        # Select all users from the users table where their user_id corresponds to a following_id of the current user
        
        # Select all entries where the user is following the current user
        followers = Following.query.filter_by(following_id=self.current_user.id).all()
        # Generate list of User objects representing list of users who are following the current user

        # Query all users in Following
        # followers = Following.query.filter(Following.following_id == self.current_user)
        followers = [
            data.to_dict_follower() for data in followers
        ]
        return Response(json.dumps(followers), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        FollowerListEndpoint, 
        '/api/followers', 
        '/api/followers/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
