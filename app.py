from flask import Flask, redirect
from Auth.auth_logic import login_is_required, user_is_logged_in, with_session, get_session_id
from Auth.database_interactions import data_handling
from Auth.config import Config

app = Flask("Random Flask App")
app.config.from_object(Config)
app.secret_key = app.config["SECRET_KEY"]


@app.route("/protected_area1")
@login_is_required
@with_session
def protected_area1():
    return "This is protected_area1. Welcome"


@app.route("/protected_area2")
@login_is_required
@with_session
def protected_area2():
    return "This is protected_area2. Welcome"


@app.route("/unprotected_area")
@with_session
def unprotected_area():
    if user_is_logged_in():
        return "Welcome to this test app index page <a href='/logout'><button>Logout</button></a> " \
               "<a href='/unprotected_area'><button>Unprotected Area</button></a> " \
               "<a href='/protected_area1'><button>Protected Area 1</button></a> " \
               "<a href='/protected_area2'><button>Protected Area 2</button></a> " \
               "<a href='/callback'><button>Callback</button></a>"
    else:
        return "Welcome to this test app index page <a href='/login'><button>Login</button></a> " \
               "<a href='/unprotected_area'><button>Unprotected Area</button></a> " \
               "<a href='/protected_area1'><button>Protected Area 1</button></a> " \
               "<a href='/protected_area2'><button>Protected Area 2</button></a> " \
               "<a href='/callback'><button>Callback</button></a>"


@app.route("/")
@with_session
def index():
    session_object = data_handling.Session(get_session_id())
    if session_object.email is not None:
        email = session_object.email
    else:
        email = "blank text"
    if session_object.in_login:
        return redirect("/callback")
    if user_is_logged_in():
        return "Welcome to this test app index page. Your email is " + \
               email + \
               " <a href='/logout'><button>Logout</button></a> " \
               "<a href='/unprotected_area'><button>Unprotected Area</button></a> " \
               "<a href='/protected_area1'><button>Protected Area 1</button></a> " \
               "<a href='/protected_area2'><button>Protected Area 2</button></a> " \
               "<a href='/callback'><button>Callback</button></a>"
    else:
        return "Welcome to this test app index page <a href='/login'><button>Login</button></a> " \
               "<a href='/unprotected_area'><button>Unprotected Area</button></a> " \
               "<a href='/protected_area1'><button>Protected Area 1</button></a> " \
               "<a href='/protected_area2'><button>Protected Area 2</button></a> " \
               "<a href='/callback'><button>Callback</button></a>"
