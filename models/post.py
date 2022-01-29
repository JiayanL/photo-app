from datetime import datetime
import random
from . import db

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.Text, nullable=True)
    alt_text = db.Column(db.Text, nullable=True)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'),
        nullable=False)

    # read-only property for referencing User properties
    user = db.relationship('User', backref="posts", lazy=False)
    comments = db.relationship('Comment', cascade="all,delete-orphan", lazy='select',
        backref=db.backref('posts', lazy='joined'))

    def __init__(self, image_url, user_id, caption=None, alt_text=None, pub_date=None):
        self.image_url = image_url
        self.user_id = user_id
        self.caption = caption
        self.alt_text = alt_text
        self.pub_date = pub_date

    def __repr__(self):
        return '<Post={0} by User={1}>'.format(self.id, self.user_id)

    def to_dict(self, include_comments=True): 
        d = {
            'id': self.id,
            'image_url': self.image_url,
            'user': self.user.to_dict(),
            'caption': self.caption, 
            'alt_text': self.alt_text
        }
        if include_comments:
            d['comments'] = [
                comment.to_dict() for comment in self.comments
            ]
        return d
 