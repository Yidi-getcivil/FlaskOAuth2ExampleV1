from flask import session, redirect, url_for
from flask_dance.contrib.atlassian import make_atlassian_blueprint, atlassian
from flask_dance.contrib.azure import make_azure_blueprint, azure
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
        return "Welcome to this test app login page " \
               "<a href='/login_with_google'><button>Login with Google</button></a>" \
               " <a href='/login_with_github'><button>Login with GitHub</button></a> " \
               "<a href='/login_with_azure'><button>Login with Azure</button></a> " \
               "<a href='/login_with_atlassian'><button>Login with Atlassian</button></a>"


@app.route("/logout")
def logout():
    session_object = data_handling.Session(get_session_id())
    session.clear()
    session_object.logout()
    return redirect("/callback")


@app.route("/callback")
def callback():
    session_object = data_handling.Session(get_session_id())
    session_object.set_out_login()
    if session_object.provider == "github_incomplete":
        return redirect("/login_with_github")
    if session_object.provider == "google_incomplete":
        return redirect("/login_with_google")
    if session_object.provider == "azure_incomplete":
        return redirect("/login_with_azure")
    if session_object.provider == "atlassian_incomplete":
        return redirect("/login_with_atlassian")

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

