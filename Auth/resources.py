import json
import os
from flask import session, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google

from Auth.auth_logic import user_is_logged_in, get_session_id
from Auth.database_interactions import data_handling
from app import app


@app.route("/login")
def login():
    session_object = data_handling.Session(get_session_id())
    session_object.set_in_login()
    if user_is_logged_in():
        return redirect("/callback")
    else:
        return "Welcome to this test app login page <a href='/login_with_google'><button>Login with Google</button></a>" \
               " <a href='/login_with_github'><button>Login with GitHub</button></a>"


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


with open('Auth/credentials/google_secrets.json', "r") as f:
    google_secrets = json.load(f)


@app.route("/callback")
def callback():
    session_object = data_handling.Session(get_session_id())
    session_object.set_out_login()
    if session_object.provider == "github_incomplete":
        return redirect("/login_with_github")
    if session_object.provider == "google_incomplete":
        return redirect("/login_with_google")

    return redirect(session_object.most_recent_source_route)


@app.route("/logout")
def logout():
    session_object = data_handling.Session(get_session_id())
    session.clear()
    session_object.logout()
    return redirect("/callback")


github_blueprint = make_github_blueprint(client_id='Iv1.f478aaf7768f3cb6',
                                         client_secret='e2d3f974d4d048c936ddde11b4ef64c8245e6d7f')

app.register_blueprint(github_blueprint, url_prefix='/github_login', redirect_to="callback",
                       login_url="/login_with_github")


@app.route("/login_with_github")
def github_login():
    session_object = data_handling.Session(get_session_id())
    if not github.authorized:
        session_object.set_in_login()
        session_object.provider = "github_incomplete"
        session_object.save()
        return redirect(url_for("github.login"))

    # Check if user is authorized with GitHub
    provider_authorized = github.authorized

    account_info = github.get("/user")
    account_info_json = account_info.json()
    session_object.add_id_info("github", account_info_json, provider_authorized)

    return redirect("/callback")


google_blueprint = make_google_blueprint(
    client_id='804316319918-rm70scnbrahencq3nn4l4qrhmkj3ni03.apps.googleusercontent.com',
    client_secret='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',
    scope=["https://www.googleapis.com/auth/userinfo.email",
           "openid",
           "https://www.googleapis.com/auth/userinfo.profile"])

app.register_blueprint(google_blueprint, url_prefix='/google_login', redirect_to="callback",
                       login_url="/login_with_google")


@app.route("/login_with_google")
def google_login():
    session_object = data_handling.Session(get_session_id())
    if not google.authorized:
        session_object.set_in_login()
        session_object.provider = "google_incomplete"
        session_object.save()
        return redirect(url_for("google.login"))

    account_info = google.get("/oauth2/v1/userinfo")
    account_info_json = account_info.json()
    provider_authorized = google.authorized
    session_object.add_id_info("google", account_info_json, provider_authorized)

    return redirect("/callback")
