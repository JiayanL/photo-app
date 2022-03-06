from flask import Response
from flask_restful import Resource
from models import LikePost, db, Post
import json

from my_decorators import handle_db_insert_error
from . import can_view_post
import flask_jwt_extended

class PostLikesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    @handle_db_insert_error
    def post(self, post_id):
        # retrieve information for post
        user_id = self.current_user.id 
            
        # Checks
        # check that post id format is valid (400)
        try:  
            int(post_id)
        except:
            return Response(json.dumps({'message': 'post id is not an int'}), mimetype="application/json", status=400)
        # check that post id is valid
        check_post = Post.query.get(post_id)
        if not check_post:
            return Response(json.dumps({'message': 'Error: Post id is not valid - post does not exist'}), mimetype="application/json", status=404)
        # check that we have access to post (404)
        if not can_view_post(post_id, self.current_user):
            return Response(json.dumps({'message': 'Error: User does not have access to this post'}), mimetype="application/json", status=404)

        # post information to comments
        like = LikePost(user_id,post_id)
        db.session.add(like)
        db.session.commit()
        return Response(json.dumps(like.to_dict()), mimetype="application/json", status=201)

class PostLikesDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def delete(self, post_id, id):
        # check that format is valid
        try: 
            int(post_id)
            int(id)
        except:
            return Response(json.dumps({'message': 'Error: Missing post id'}), mimetype="application/json", status=400)
        # check that id is valid
        liked_post = LikePost.query.get(id)
        if not (liked_post and Post.query.get(post_id)):
            return Response(json.dumps({'message': 'Error: Id is not valid'}), mimetype="application/json", status=404)
        # check that we are authorized to delete
        if int(liked_post.user_id) != int(self.current_user.id): 
            return Response(json.dumps({'message': 'Error: We are not authorized to delete'}), mimetype="application/json", status=404)
        if int(liked_post.post_id) != int(post_id):
            return Response(json.dumps({'message': 'Error: We are not authorized to delete'}), mimetype="application/json", status=404)
       
        LikePost.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message': 'Post {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        PostLikesListEndpoint, 
        '/api/posts/<post_id>/likes', 
        '/api/posts/<post_id>/likes/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )

    api.add_resource(
        PostLikesDetailEndpoint, 
        '/api/posts/<post_id>/likes/<id>', 
        '/api/posts/<post_id>/likes/<id>/',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
