from flask import Response
from flask_restful import Resource
from models import Story
from . import get_authorized_user_ids
import json

class StoriesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # get list of users who stories you would have to see
        authorized_users = get_authorized_user_ids(self.current_user)

        # get all stories where user id is in authorized users
        story_list = Story.query.filter(Story.user_id.in_(authorized_users)).all()
        # turn into dictionary
        story_list = [story.to_dict() for story in story_list]
        return Response(json.dumps(story_list), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        StoriesListEndpoint, 
        '/api/stories', 
        '/api/stories/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
