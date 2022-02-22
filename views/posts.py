from flask import Response, request
from flask_restful import Resource
from models import Post, db

from views import security, get_authorized_user_ids

import json

def get_path():
    return request.host_url + 'api/posts/'

class PostListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user

    def get(self):
        ids = get_authorized_user_ids(self.current_user)
        posts = Post.query.filter(Post.user_id.in_(ids))
        limit = request.args.get('limit')
        if limit:
            try:
                limit = int(limit)
            except:
                return Response(json.dumps({'message': 'Limit must be an integer between 1 and 50'}), mimetype="application/json", status=400)
            if limit > 50 or limit < 1:
                return Response(json.dumps({'message': 'Limit must be an integer between 1 and 50'}), mimetype="application/json", status=400)
        else:
            limit = 10
        posts = posts.order_by(Post.pub_date.desc()).limit(limit)

        # note: if you pass the current user into to_dict(), it will tell you
        # whether or not the current user liked and/or bookmarked any of the posts
        data = [
            item.to_dict(user=self.current_user) for item in posts.all()
        ]
        return Response(json.dumps(data), mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        image_url = body.get('image_url')
        if image_url is None:
            return Response(json.dumps({'message': '"image_url" is required.'}), mimetype="application/json", status=400)
        caption = body.get('caption')
        alt_text = body.get('alt_text')
        user_id = self.current_user.id # id of the user who is logged in
        
        # create post:
        post = Post(image_url, user_id, caption, alt_text)
        db.session.add(post)
        db.session.commit()
        return Response(json.dumps(post.to_dict(user=self.current_user)), mimetype="application/json", status=201)
        
class PostDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
        
    
    @security.id_is_valid
    @security.user_can_edit_post
    def patch(self, id):
        post = Post.query.get(id)
        body = request.get_json()

        post.image_url = body.get('image_url') or body.get('image_url')
        if body.get('caption') is not None:
            post.caption = body.get('caption')
        if body.get('alt_text') is not None:
            post.alt_text = body.get('alt_text')
        
        # commit changes:
        db.session.commit()        
        return Response(json.dumps(post.to_dict(user=self.current_user)), mimetype="application/json", status=200)
    
    @security.id_is_valid
    @security.user_can_edit_post
    def delete(self, id):
        Post.query.filter_by(id=id).delete()
        db.session.commit()

        serialized_data = {
            'message': 'Post {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)

    @security.id_is_valid
    @security.user_can_view_post
    def get(self, id):
        post = Post.query.get(id)
        return Response(json.dumps(post.to_dict(user=self.current_user)), mimetype="application/json", status=200)

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