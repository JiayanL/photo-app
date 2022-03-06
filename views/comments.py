from flask import Response, request
from flask_restful import Resource
from . import can_view_post
from my_decorators import handle_db_insert_error
import json
from models import db, Comment, Post
import flask_jwt_extended

class CommentListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user

    @flask_jwt_extended.jwt_required()
    @handle_db_insert_error
    def post(self):
        #check that id is right format

        # retrieve information for post
        body = request.get_json()
        post_id = body.get('post_id')
        text = body.get('text')
        user_id = self.current_user.id 

        # check that post id is not missing
        if not post_id:
            return Response(json.dumps({'message': 'Error: Missing post id'}), mimetype="application/json", status=400)
        # check that post id is valid format
        elif not isinstance(post_id, int):
            return Response(json.dumps({'message': 'Error: post id is not an int'}), mimetype="application/json", status=400)
        # check that we have authorization
        elif not can_view_post(post_id, self.current_user):
            return Response(json.dumps({'message': 'Error: User cannot view post'}), mimetype="application/json", status=404)
        # check that the post_id is valid
        elif not text:
            return Response(json.dumps({'message': 'Invalid post - no text'}), mimetype="application/json", status=400)

        # post information to comments
        comment = Comment(text, user_id, post_id)
        db.session.add(comment)
        db.session.commit()
        return Response(json.dumps(comment.to_dict()), mimetype="application/json", status=201)
        
class CommentDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
  
    @flask_jwt_extended.jwt_required()
    def delete(self, id):
        # check that format is valid
        try: 
            int(id)
        except:
            return Response(json.dumps({'message': 'Error: Missing post id'}), mimetype="application/json", status=400)
        comment = Comment.query.get(id)
         # check that id is valid
        if not comment:
            return Response(json.dumps({'message': 'Invalid post - no text'}), mimetype="application/json", status=404)
        # check that we are authorized to delete
        if not comment.user_id == self.current_user.id:
            return Response(json.dumps({'message': 'Error: User cannot view post'}), mimetype="application/json", status=404)
       
        
        Comment.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message': 'Post {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        CommentListEndpoint, 
        '/api/comments', 
        '/api/comments/',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}

    )
    api.add_resource(
        CommentDetailEndpoint, 
        '/api/comments/<id>', 
        '/api/comments/<id>',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
