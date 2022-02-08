# load the environment variables:
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template
from flask_restful import Api
import os
from models import db, User
from views import bookmarks, comments, followers, following, \
    posts, profile, stories, suggestions, post_likes

# Importing fake data
import fake_data

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False    


db.init_app(app)
api = Api(app)

# set logged in user
with app.app_context():
    app.current_user = User.query.filter_by(id=12).one()


# Initialize routes for all of your API endpoints:
bookmarks.initialize_routes(api)
comments.initialize_routes(api)
followers.initialize_routes(api)
following.initialize_routes(api)
posts.initialize_routes(api)
post_likes.initialize_routes(api)
profile.initialize_routes(api)
stories.initialize_routes(api)
suggestions.initialize_routes(api)

# Server-side template for the homepage:
@app.route('/')
def home():
    current_user = fake_data.generate_user()
    return render_template(
        'index.html', 
        user=current_user,
        posts=fake_data.generate_posts(n=8),
        stories=fake_data.generate_stories(n=6),
        suggestions=fake_data.generate_suggestions(n=7)
    )

# enables flask app to run using "python3 app.py"
if __name__ == '__main__':
    app.run()
