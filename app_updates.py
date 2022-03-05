# new import statements:
import flask_jwt_extended  
import decorators

# new views:
from views import authentication, token

#JWT config variables and manager (add after app object created):
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET')
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
app.config["JWT_COOKIE_SECURE"] = False
jwt = flask_jwt_extended.JWTManager(app)

# Initialize routes of 2 new views
authentication.initialize_routes(app)
token.initialize_routes(api)


# Updated API endpoint includes a reference to 
# access_token and csrf token.
@app.route('/api')
@decorators.jwt_or_login
def api_docs():
    access_token = request.cookies.get('access_token_cookie')
    csrf = request.cookies.get('csrf_access_token')
    navigator = ApiNavigator(flask_jwt_extended.current_user)
    return render_template(
        'api/api-docs.html', 
        user=app.current_user,  #TODO: change to flask_jwt_extended.current_user
        endpoints=navigator.get_endpoints(),
        access_token=access_token,
        csrf=csrf,
        url_root=request.url_root[0:-1] # trim trailing slash
    )