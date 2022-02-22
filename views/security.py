from models import Post, Comment
from flask import Response, request
from views import can_view_post
import json

def get_does_not_exist_response(model_name, id):
    return Response(
        json.dumps({'message': '{0} id={1} does not exist'.format(model_name, id)}), 
        mimetype="application/json", 
        status=404
    )

##############
# Decorators #
##############
def _id_is_valid(self, func, key, *args, **kwargs):
    try:
        body = request.get_json()
        # if int parse is successful, then id is valid it:
        # print(key, args, kwargs)
        int(kwargs.get(key) or body.get(key))
    except:
        return Response(
            json.dumps({'message': 'Invalid {0}={1}'.format(key, kwargs.get(key))}), 
            mimetype="application/json", 
            status=400
        )
    return func(self, *args, **kwargs)

def id_is_valid(func):
    def wrapper(self, *args, **kwargs):
        return _id_is_valid(self, func, 'id', *args, **kwargs)
    return wrapper

def post_id_is_valid(func):
    def wrapper(self, *args, **kwargs):
        return _id_is_valid(self, func, 'post_id', *args, **kwargs)
    return wrapper

def user_id_is_valid(func):
    def wrapper(self, *args, **kwargs):
        return _id_is_valid(self, func, 'user_id', *args, **kwargs)
    return wrapper


def user_can_view_post(func):
    def wrapper(self, *args, **kwargs):
        body = request.get_json()
        id = kwargs.get('id') or kwargs.get('post_id') or body.get('post_id')
        if (can_view_post(id, self.current_user)):
            return func(self, *args, **kwargs)
        else:
            return get_does_not_exist_response('Post', id)
    return wrapper

def user_can_edit_post(func):
    def wrapper(self, *args, **kwargs):
        body = request.get_json()
        id = kwargs.get('id') or kwargs.get('post_id') or body.get('post_id')
        post = Post.query.get(id)
        if not post or post.user_id != self.current_user.id:
            return get_does_not_exist_response('Post', id)
        else:
            return func(self, *args, **kwargs)
    return wrapper

def user_can_edit_comment(func):
    def wrapper(self, *args, **kwargs):
        comment = Comment.query.get(kwargs.get('id'))
        if not comment or comment.user_id != self.current_user.id:
            return get_does_not_exist_response('Comment', kwargs.get('id'))
        else:
            return func(self, *args, **kwargs)
    return wrapper

