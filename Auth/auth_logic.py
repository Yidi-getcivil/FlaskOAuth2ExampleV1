import random
import string
from flask import session, abort, request
from functools import wraps
from Auth.database_interactions import data_handling
from Auth.database_interactions.data_handling import Session


def with_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_id = get_session_id()
        session_object = Session(session_id)

        if not (session_object.in_login and request.path == "/"):

            # Update the most_recent_source_route with the current endpoint
            most_recent_source_route = request.path
            session_object.most_recent_source_route = most_recent_source_route
            session_object.set_out_login()
            session_object.save()

        # Call the endpoint function with the session object as an argument
        return f(*args, **kwargs)
    return decorated_function


def get_session_id():
    if 'session_id' in session:
        return session['session_id']
    else:
        session_id = generate_session_id()
        session['session_id'] = session_id
        return session_id


def generate_session_id(length=20):
    # Generate a random string of alphanumeric characters
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def user_is_logged_in():
    session_object = data_handling.Session(get_session_id())
    if session_object.provider_authorized:
        return True
    else:
        return False


def login_is_required(function):
    def wrapper():
        if user_is_logged_in():
            return function()
        else:
            return abort(401)
    wrapper.__name__ = function.__name__  # Set the name of the wrapper function to the name of the original function
    return wrapper
