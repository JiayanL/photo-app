from flask import Response, request
from flask_restful import Resource
from models import Following, User, db
import json

from my_decorators import handle_db_insert_error

def get_path():
    return request.host_url + 'api/posts/'

class FollowingListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # Get users who current uesr is following with data model
        following = Following.query.filter_by(user_id=self.current_user.id).all()

        # Convert into user profiles
        following = [
            data.to_dict_following() for data in following
        ]
        return Response(json.dumps(following), mimetype="application/json", status=200)
    
    @handle_db_insert_error
    def post(self):
        # retrieve information for post
        body = request.get_json()
        following_id = body.get('user_id')
        user_id = self.current_user.id 

        # check for invalid format
        if not isinstance(int(following_id), int):
            return Response(json.dumps({'message': 'error invalid format'}), mimetype="application/json", status=400)
        # check for missing user id
        if not following_id or not body:
            return Response(json.dumps({'message': 'missing id'}), mimetype="application/json", status=400)
        # check for invalid user id
        followed_user = User.query.get(following_id)
        if not followed_user:
            return Response(json.dumps({'message': 'missing id'}), mimetype="application/json", status=404)
        # check for no duplicates

        # post information to comments
        following = Following(user_id, following_id)
        db.session.add(following)
        db.session.commit()
        return Response(json.dumps(following.to_dict_following()), mimetype="application/json", status=201)


class FollowingDetailEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
         # check that format is valid
        try: 
            int(id)
        except:
            return Response(json.dumps({'message': 'Error: Missing post id'}), mimetype="application/json", status=400)
        followed = Following.query.get(id)
         # check that id is valid
        if not followed:
            return Response(json.dumps({'message': 'Invalid post - no text'}), mimetype="application/json", status=404)
        # check that we are authorized to delete
        if not followed.user_id == self.current_user.id:
            return Response(json.dumps({'message': 'Error: User cannot view post'}), mimetype="application/json", status=404)
       
        
        Following.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message': 'Post {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        FollowingListEndpoint, 
        '/api/following', 
        '/api/following/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        FollowingDetailEndpoint, 
        '/api/following/<id>', 
        '/api/following/<id>/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
