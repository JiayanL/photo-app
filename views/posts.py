from flask import Response, request
from flask_restful import Resource
from models import Post, User, db
from my_decorators import handle_db_insert_error
from . import can_view_post, get_authorized_user_ids
import json
from sqlalchemy import and_

def get_path():
    return request.host_url + 'api/posts/'

class PostListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user

    def get(self):
        # 1. Security -> User has access to post if they
        # a. Created post themselves
        # b. They are following a user who created the post

        # Get list of authorized users based on who the current user is
        authorized_ids = get_authorized_user_ids(self.current_user)
        # Query all posts that are posted by authorized users
        posts = Post.query.filter(Post.user_id.in_(authorized_ids))

        # 2. Create limits for query parameter
        # Extract limit argument from the HTTP request
        limit = request.args.get('limit')

        # Check that query is legitimate and edit - limit error checking
        if limit:
            try: 
                limit = int(limit)
            except:
                return Response(json.dumps({'message': 'Limit must be an integer betweeen 1 and 50'}), mimetype="application/json", status=400)
            if limit > 50 or limit <1:
                return Response(json.dumps({'message': 'Limit must be an integer between 1 and 50'}), mimetype="application/json", status=400)
        # Default limit is 10
        else:
            limit = 10
        
        # order lists of posts by publication date
        posts = posts.order_by(Post.pub_date.desc())
        # Query data with limit
        data = posts.limit(limit).all()

        # to dict converts each item in data into a JSON object based on function we have
        data = [
            item.to_dict() for item in data
        ]
        return Response(json.dumps(data), mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        image_url = body.get('image_url')
        caption = body.get('caption')
        alt_text = body.get('alt_text')
        user_id = self.current_user.id # id of the user who is logged in
        
        # check that post is not empty and that post contains a caption
        if body is None:
            return Response(json.dumps({'message': 'Error. Missing body to post.'}), mimetype="application/json", status=404)
        elif image_url is None:
            return Response(json.dumps({'message': 'Error, post is just an image. Post needs caption'}), mimetype="application/json", status=400)
       
        # create post:
        post = Post(image_url, user_id, caption, alt_text)
        db.session.add(post)
        db.session.commit()
        return Response(json.dumps(post.to_dict()), mimetype="application/json", status=201)
        
class PostDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
        
    def patch(self, id):
        # post = Post.query.get(id)
        # Query post nand make sure its valid
        try:
            post = Post.query.get(id)
        except:
            return Response(json.dumps({'message': 'Post does not exist'}), mimetype="application/json", status=400)
        
        # a user can only edit their own post:
        if not post:
            return Response(json.dumps({'message': 'Post does not exist'}), mimetype="application/json", status=404)
        if post.user_id != self.current_user.id:
            return Response(json.dumps({'message': 'User does not have access to this post'}), mimetype="application/json", status=404)

        body = request.get_json()
        post.image_url = body.get('image_url') or post.image_url
        post.caption = body.get('caption') or post.caption
        post.alt_text = body.get('alt_text') or post.alt_text
        
        # commit changes:
        db.session.commit()        
        return Response(json.dumps(post.to_dict()), mimetype="application/json", status=200)
    
    def delete(self, id):

        # a user can only delete their own post:
        try:
            post = Post.query.get(id)
        except:
            return Response(json.dumps({'message': 'Post does not exist'}), mimetype="application/json", status=400)
        
        if not post or post.user_id != self.current_user.id:
            return Response(json.dumps({'message': 'Post does not exist'}), mimetype="application/json", status=404)
       

        Post.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message': 'Post {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)
        
    def get(self, id):
        try:
            post = Post.query.get(id)
        except:
            return Response(json.dumps({'message': 'id is invaild'}), mimetype="application/json", status=400)

        # if the user is not allowed to see the post or if the post does not exist, return 404:
        if not post or not can_view_post(post.id, self.current_user):
            return Response(json.dumps({'message': 'Post does not exist'}), mimetype="application/json", status=404)
        
        return Response(json.dumps(post.to_dict()), mimetype="application/json", status=200)

def initialize_routes(api):
    api.add_resource(
        PostListEndpoint, 
        '/api/posts', '/api/posts/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        PostDetailEndpoint, 
        '/api/posts/<id>', '/api/posts/<id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )