import hashlib
import sqlite3
from flask import session, redirect, url_for, request, render_template
from flask_dance.contrib.atlassian import make_atlassian_blueprint, atlassian
from flask_dance.contrib.azure import make_azure_blueprint, azure
from flask_dance.contrib.dropbox import make_dropbox_blueprint, dropbox
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google
import constants
from Auth.auth_logic import user_is_logged_in, get_session_id, is_valid_email
from Auth.database_interactions import data_handling
from Auth.database_interactions.data_handling import InternalAuthUser
from app import app


@app.route("/login")
def login():
    session_object = data_handling.Session(get_session_id())
    session_object.set_in_login()
    if user_is_logged_in():
        return redirect("/callback")
    else:
        return render_template(
            "client_login.html",
            base_url=constants.BASE_URL,
            request_secret=session_object.create_new_request_secret()
        )


@app.route("/signup_begin")
def signup_begin():
    session_object = data_handling.Session(get_session_id())
    session_object.set_in_login()
    if user_is_logged_in():
        return redirect("/callback")
    else:
        return render_template(
            "client_signup_begin.html",
            base_url=constants.BASE_URL,
            request_secret=session_object.create_new_request_secret()
        )


@app.route("/signup_end/<email>")
def signup_end(email):
    session_object = data_handling.Session(get_session_id())
    session_object.set_in_login()
    user = InternalAuthUser.get_user_by_email(email)
    if user_is_logged_in():
        return redirect("/callback")
    else:
        return render_template(
            "client_signup_end.html",
            base_url=constants.BASE_URL,
            request_secret=session_object.create_new_request_secret(),
            email=user.email,
            salt=user.client_salt
        )


@app.route("/logout")
def logout():
    session_object = data_handling.Session(get_session_id())
    session.clear()
    session_object.logout()
    return redirect("/callback")


@app.route("/create_email_login", methods=["POST"])
def create_email_login():
    session_object = data_handling.Session(get_session_id())
    session_object.set_in_login()
    if user_is_logged_in():
        return redirect("/callback")

    email = request.form.get("email")

    # Check if there is already a user completed with that email
    if InternalAuthUser.email_exists_and_completed(email):
        return "Error: User with email already exists and is completed", 409

    # Get the user using the email
    user = InternalAuthUser.get_user_by_email(email)

    # If user does not exist, create the user
    if user is None:
        # Check if email address is valid
        if not is_valid_email(email):
            return "Error: Invalid email address", 400

        # Create user
        user = InternalAuthUser.create_user(email)
        return "Success", 200

    return "Success", 200


@app.route("/signup", methods=["POST"])
def sign_up_internal():
    session_object = data_handling.Session(get_session_id())
    session_object.set_in_login()
    if user_is_logged_in():
        return redirect("/callback")

    email = request.form.get("email")
    first_name = request.form.get("first_name")
    middle_name = request.form.get("middle_name", "")
    last_name = request.form.get("last_name")
    hashed_password = request.form.get("hashed_password")

    # Check if there is already a user completed with that email
    if InternalAuthUser.email_exists_and_completed(email):
        return "Error: User with email already exists and is completed", 409

    # Get the user using the email
    user = InternalAuthUser.get_user_by_email(email)

    if None in [email, first_name, middle_name, last_name, hashed_password]:
        return "Error: Missing required fields", 400

    user.update_user_info(first_name, middle_name, last_name, hashed_password)
    session_object.add_id_info(
        "erasetheline",
        {
            "email": user.email,
            "email_verified": True,
            "given_name": user.first_name,
            "family_name": user.last_name,
            "id": user.user_id
        },
        True
    )

    return "Success", 200


@app.route("/salt_request", methods=["POST"])
def salt_request():
    session_object = data_handling.Session(get_session_id())
    session_object.set_in_login()
    if user_is_logged_in():
        return redirect("/callback")

    email = request.form.get("email")

    # Get the user using the email
    user = InternalAuthUser.get_user_by_email(email)

    if user is None:
        return "Error: No such Email", 400

    return {
        "email": user.email,
        "salt": user.client_salt,
        "request_secret": session_object.request_secret
    }


@app.route("/internal_login", methods=["POST"])
def internal_login():
    session_object = data_handling.Session(get_session_id())
    session_object.set_in_login()
    if user_is_logged_in():
        return redirect("/callback")

    email = request.form.get("email")
    hashed_password = request.form.get("password")

    # Get the user using the email
    user = InternalAuthUser.get_user_by_email(email)

    if user is None:
        return "Error: No such Email", 400

    provider_authorized = user.check_password(hashed_password)
    if provider_authorized:
        session_object.add_id_info(
            "erasetheline",
            {
                "email": user.email,
                "email_verified": True,
                "given_name": user.first_name,
                "family_name": user.last_name,
                "id": user.user_id
            },
            True
        )
    else:
        return "Error: Incorrect Password", 400

    return "Success", 200


@app.route("/callback")
def callback():
    session_object = data_handling.Session(get_session_id())
    session_object.set_out_login()
    if session_object.provider is None:
        return redirect(session_object.most_recent_source_route)
    if session_object.provider.endswith("_incomplete"):
        provider_name = session_object.provider[:-11]  # remove "_incomplete" suffix from provider name
        return redirect(f"/login_with_{provider_name}")
    else:
        return redirect(session_object.most_recent_source_route)


github_blueprint = make_github_blueprint(client_id=app.config["GITHUB_OAUTH_CLIENT_ID"],
                                         client_secret=app.config["GITHUB_OAUTH_CLIENT_SECRET"],
                                         redirect_to="callback",
                                         login_url="/login_with_github")
app.register_blueprint(github_blueprint, url_prefix='/github_login')


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
    client_id=app.config["GOOGLE_OAUTH_CLIENT_ID"],
    client_secret=app.config["GOOGLE_OAUTH_CLIENT_SECRET"],
    scope=["https://www.googleapis.com/auth/userinfo.email",
           "openid",
           "https://www.googleapis.com/auth/userinfo.profile"],
    redirect_to="callback",
    login_url="/login_with_google")
app.register_blueprint(google_blueprint, url_prefix='/google_login')


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


azure_blueprint = make_azure_blueprint(
    client_id=app.config["AZURE_OAUTH_CLIENT_ID"],
    client_secret=app.config["AZURE_OAUTH_CLIENT_SECRET"],
    tenant=app.config["AZURE_OAUTH_TENANT"],
    scope=["User.Read"],
    redirect_to="callback",
    login_url="/login_with_azure"
)
app.register_blueprint(azure_blueprint, url_prefix='/azure_login')


@app.route("/login_with_azure")
def azure_login():
    session_object = data_handling.Session(get_session_id())
    if not azure.authorized:
        session_object.set_in_login()
        session_object.provider = "azure_incomplete"
        session_object.save()
        return redirect(url_for("azure.login"))

    account_info = azure.get("/v1.0/me")
    account_info_json = account_info.json()
    provider_authorized = azure.authorized
    session_object.add_id_info("azure", account_info_json, provider_authorized)

    return redirect("/callback")


atlassian_blueprint = make_atlassian_blueprint(
    client_id=app.config["ATLASSIAN_OAUTH_CLIENT_ID"],
    client_secret=app.config["ATLASSIAN_OAUTH_CLIENT_SECRET"],
    scope=["offline_access", "read:jira-user", "read:jira-work", "write:jira-work"],
    redirect_to="callback",
    login_url="/login_with_atlassian"
)
app.register_blueprint(atlassian_blueprint, url_prefix='/atlassian_login')


@app.route("/login_with_atlassian")
def atlassian_login():
    session_object = data_handling.Session(get_session_id())
    if not atlassian.authorized:
        session_object.set_in_login()
        session_object.provider = "atlassian_incomplete"
        session_object.save()
        return redirect(url_for("atlassian.login"))

    account_info = atlassian.get("/rest/api/3/myself")
    account_info_json = account_info.json()
    provider_authorized = atlassian.authorized
    session_object.add_id_info("atlassian", account_info_json, provider_authorized)

    return redirect("/callback")


dropbox_blueprint = make_dropbox_blueprint(
    app_key=app.config["DROPBOX_OAUTH_APP_KEY"],
    app_secret=app.config["DROPBOX_OAUTH_APP_SECRET"],
    scope=["account_info.read", "sharing.read"],
)
app.register_blueprint(dropbox_blueprint, url_prefix='/dropbox_login')


@app.route("/login_with_dropbox")
def dropbox_login():
    session_object = data_handling.Session(get_session_id())
    if not dropbox.authorized:
        session_object.set_in_login()
        session_object.provider = "dropbox_incomplete"
        session_object.save()
        return redirect(url_for("dropbox.login"))

    account_info = dropbox.get("/users/get_account")
    account_info_json = account_info.json()
    provider_authorized = dropbox.authorized
    session_object.add_id_info("dropbox", account_info_json, provider_authorized)

    return redirect("/callback")
