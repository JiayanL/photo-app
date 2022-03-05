from flask import (
    request, make_response, render_template, redirect
)
from models import User
import flask_jwt_extended

def logout():
    # hint:  https://dev.to/totally_chase/python-using-jwt-in-cookies-with-a-flask-app-and-restful-api-2p75
    return 'Implement Logout functionality'

def login():
    if request.method == 'POST':
        # authenticate user here. If the user sent valid credentials, set the
        # JWT cookies:
        # https://flask-jwt-extended.readthedocs.io/en/3.0.0_release/tokens_in_cookies/

        # extract username and password out of form request
        username = request.form.get('username')
        password = request.form.get('password')

        # Handle missing username and passwords
        if not username:
            return render_template(
                'login.html', 
                message='Missing username'
            )
        if not password:
            return render_template(
                'login.html', 
                message='Missing password'
            )
        
        # Procede with database checks
        # returns user object or nothing
        user = User.query.filter_by(username=username).one_or_none()
        if user:
            # check the password with convenience method
            if user.check_password(password):
                print('the user is authenticated')
                # create JWT access tokens to send back to user by encoding user ID in JWT
                access_token = flask_jwt_extended.create_access_token(identity=user.id)
            
                # Set the JWT cookies in the response
                # redirect to home screen through response
                response = make_response(redirect('/'))
                # put response in header
                flask_jwt_extended.set_access_cookies(response, access_token)
                return response
                
            else:
                return render_template(
                    'login.html', 
                    message='Invalid password'
                )
        else:
            return render_template(
                'login.html', 
                message='User does not exist'
            )
    else:
        return render_template(
            'login.html'
        )

def initialize_routes(app):
    app.add_url_rule('/login', 
        view_func=login, methods=['GET', 'POST'])
    app.add_url_rule('/logout', view_func=logout)