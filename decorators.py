import flask_jwt_extended
from flask import redirect

def jwt_or_login(view_function):
    def wrapper(*args, **kwargs):
        try:
            flask_jwt_extended.verify_jwt_in_request()
            return view_function(*args, **kwargs)
        except:
            return redirect('/login', code=302)
            
    # https://stackoverflow.com/questions/17256602/assertionerror-view-function-mapping-is-overwriting-an-existing-endpoint-functi
    wrapper.__name__ = view_function.__name__
    return wrapper 