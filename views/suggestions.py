from flask import Response, request
from flask_restful import Resource
from models import User, Following
from . import get_authorized_user_ids
import json
import flask_jwt_extended


class SuggestionsListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):
        # Get user and all users user is following
        authorized_users = get_authorized_user_ids(self.current_user)

        # Selects all users that aren't authorized
        suggested = User.query.filter(User.id.not_in(authorized_users))
        
        # Limits them to 7
        suggested = suggested.limit(7).all()
        
        # Converts to dictionary and returns
        suggested_users = [user.to_dict() for user in suggested]
        return Response(json.dumps(suggested_users), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        SuggestionsListEndpoint, 
        '/api/suggestions', 
        '/api/suggestions/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
