from flask import Response, request
from flask_restful import Resource
from models import Bookmark, db
import json
from . import can_view_post
from my_decorators import check_ownership_of_bookmark, handle_db_insert_error, secure_method
import flask_jwt_extended

class BookmarksListEndpoint(Resource):
    # 1. List all Resources
    # 2. Create new resources
    # Have access to user who accessed this data
    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):
        '''
        Goal is to only show the bookmarks that are associated with the current user. Approach:
            1. Use SQL Alchemy to execute the query using the "Bookmark" model (from models folder).
            2. When we return this list, it's serialized using JSON.
        '''
        # query.filter_by() same thing as WHERE clause
        bookmarks = Bookmark.query.filter_by(user_id=self.current_user.id).all()
        # print(bookmarks)

        # Convrt list of bookmark models to a list of dictionaries
        bookmark_list_of_dictionaries = [
            bookmark.to_dict() for bookmark in bookmarks
        ]
        return Response(json.dumps(bookmark_list_of_dictionaries), mimetype="application/json", status=200)

    @flask_jwt_extended.jwt_required()
    @handle_db_insert_error
    def post(self):
        '''
        Goal:
            1. Get the post_id from the request body
            2. Check that the user is authorized to bookmark the post
            3. Check that the post_id exists and is valid
            4. If 1, 2, & 3: isnsert to database
            5. Return the new bookmarked post and bookmarked id 
                to the user as part of the the response.
        '''
        # request from flasks gives you access to request from user
        # this is data that user sent
        body = request.get_json()
        # print(body)
        post_id = body.get('post_id')
        
        # to create bookmark, you need to pass it a user id and a post id
        bookmark = Bookmark(self.current_user.id, post_id)
        
        # check that we have a post id
        if not post_id:
            return Response(json.dumps({'message': 'error, missing post!!'}), mimetype="application/json", status=400)
        # check that post is valid
        if not can_view_post(post_id, self.current_user):
            return Response(json.dumps({'message': 'post id is invalid'}), mimetype="application/json", status=404)

        # save bookmark to database ('commit') new record to database
        db.session.add(bookmark)
        db.session.commit()

        # create model instance
        return Response(json.dumps(bookmark.to_dict()), mimetype="application/json", status=201)


class BookmarkDetailEndpoint(Resource):
    # 1. PATCH (updating), GET (individual bookmarks), DELETE (individual bookmarks)
    # 2. Create a new bookmark
    def __init__(self, current_user):
        self.current_user = current_user

    @flask_jwt_extended.jwt_required()
    def delete(self, id):
        # Check that id is valid
        try:
            bookmark = Bookmark.query.get(id)
        except:
            return Response(json.dumps({'message': 'bookmark does not exist'}), mimetype="application/json", status=400)
        # Check that id is valid
        if not bookmark:
            return Response(json.dumps({'message': 'User cannot delete bookmark'}), mimetype="application/json", status=404)
        # Check that user has access to post
        if bookmark.user_id != self.current_user.id:
            return Response(json.dumps({'message': 'User cannot access bookmark'}), mimetype="application/json", status=404)
        
        # Delete bookmarks
        Bookmark.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message': 'Post {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        BookmarksListEndpoint, 
        '/api/bookmarks', 
        '/api/bookmarks/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )

    api.add_resource(
        BookmarkDetailEndpoint, 
        '/api/bookmarks/<id>', 
        '/api/bookmarks/<id>',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
