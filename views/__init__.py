from models import db, Following, Post
from sqlalchemy import and_

'''
Below are some helper functions to help you with security:
'''

def get_authorized_user_ids(current_user):
    # query the "following" table to get the list of authorized users:
    user_ids_tuples = (
        db.session
            .query(Following.following_id)
            .filter(Following.user_id == current_user.id)
            .order_by(Following.following_id)
            .all()
    )
    # convert to a list of ints:
    user_ids = [id for (id,) in user_ids_tuples]

    # don't forget to add the current user:
    user_ids.append(current_user.id)
    return user_ids

def can_view_post(post_id, user):
    # find user_ids that the user can follow (including the user themselves)
    auth_users_ids = get_authorized_user_ids(user)

    # query for all the posts that are owned by the user:
    post = Post.query.filter(and_(Post.id==post_id, Post.user_id.in_(auth_users_ids))).first()
    if not post:
        return False
    return True
        