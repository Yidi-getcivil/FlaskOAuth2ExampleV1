# Create a connection to the database
import pickle
import random
import sqlite3
import string
from datetime import datetime, timedelta
from Auth.database_interactions import create_table
from passlib.hash import argon2

create_table.create_sessions_table()
create_table.create_users_auth_table()


# Define the Session class
class Session:
    def __init__(self, session_id):
        self.session_id = session_id
        conn = sqlite3.connect('sessions.db')
        cursor = conn.cursor()
        results = cursor.execute('SELECT * FROM sessions WHERE session_id = ?;', (self.session_id,))
        row = results.fetchone()
        conn.close()
        if row:
            (
                self.session_id, self.request_secret, self.state, self.most_recent_source_route, self.datetime_created,
                self.in_login, self.provider, self.provider_authorized, self.iss, self.azp, self.aud, self.sub,
                self.email, self.email_verified, self.at_hash, self.name, self.picture, self.given_name,
                self.family_name, self.locale, self.iat, self.exp, self.login, self.id, self.node_id, self.avatar_url,
                self.gravatar_id, self.url, self.html_url, self.followers_url, self.following_url, self.gists_url,
                self.starred_url, self.subscriptions_url, self.organizations_url, self.repos_url, self.events_url,
                self.received_events_url, self.type, self.site_admin, self.company, self.blog, self.location,
                self.hireable, self.bio, self.twitter_username, self.public_repos, self.public_gists, self.followers,
                self.following, self.created_at, self.updated_at, self.context, self.businessPhones, self.displayName,
                self.givenName, self.jobTitle, self.mail, self.mobilePhone, self.officeLocation, self.preferredLanguage,
                self.surname, self.userPrincipalName, self.self, self.accountId, self.emailAddress, self.avatarUrls,
                self.active, self.timeZone, self.accountType, self.account_id, self.familiar_name, self.display_name,
                self.abbreviated_name, self.disabled, self.country, self.referral_link, self.team, self.account_type,
                self.root_info, self.profile_photo_url, self.membership_type, self.team_member_id, self.is_paired,
                self.account_migration_state
             ) = row
            self.businessPhones = pickle.loads(self.businessPhones)
            self.avatarUrls = pickle.loads(self.avatarUrls)
            self.team = pickle.loads(self.team)
            self.account_type = pickle.loads(self.account_type)
            self.root_info = pickle.loads(self.root_info)
            self.membership_type = pickle.loads(self.membership_type)
            self.account_migration_state = pickle.loads(self.account_migration_state)
        else:
            self.request_secret = None
            self.state = None
            self.most_recent_source_route = "/"
            self.datetime_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.in_login = False
            self.provider = None
            self.provider_authorized = False
            self.iss = None
            self.azp = None
            self.aud = None
            self.sub = None
            self.email = None
            self.email_verified = False
            self.at_hash = None
            self.name = None
            self.picture = None
            self.given_name = None
            self.family_name = None
            self.locale = None
            self.iat = None
            self.exp = None
            self.login = None
            self.id = None
            self.node_id = None
            self.avatar_url = None
            self.gravatar_id = None
            self.url = None
            self.html_url = None
            self.followers_url = None
            self.following_url = None
            self.gists_url = None
            self.starred_url = None
            self.subscriptions_url = None
            self.organizations_url = None
            self.repos_url = None
            self.events_url = None
            self.received_events_url = None
            self.type = None
            self.site_admin = None
            self.company = None
            self.blog = None
            self.location = None
            self.hireable = None
            self.bio = None
            self.twitter_username = None
            self.public_repos = None
            self.public_gists = None
            self.followers = None
            self.following = None
            self.created_at = None
            self.updated_at = None
            self.context = None
            self.businessPhones = []
            self.displayName = None
            self.givenName = None
            self.jobTitle = None
            self.mail = None
            self.mobilePhone = None
            self.officeLocation = None
            self.preferredLanguage = None
            self.surname = None
            self.userPrincipalName = None
            self.self = None
            self.accountId = None
            self.emailAddress = None
            self.avatarUrls = {}
            self.active = False
            self.timeZone = None
            self.accountType = None
            self.account_id = None
            self.familiar_name = None
            self.display_name = None
            self.abbreviated_name = None
            self.disabled = False
            self.country = None
            self.referral_link = None
            self.team = {}
            self.account_type = {}
            self.root_info = {}
            self.profile_photo_url = None
            self.membership_type = {}
            self.team_member_id = None
            self.is_paired = None
            self.account_migration_state = {}
        self.save()

    def save(self):
        # Save the current state of the session to the database
        query = f'''INSERT OR REPLACE INTO sessions 
        (session_id, request_secret, state, most_recent_source_route, datetime_created, in_login, provider, 
        provider_authorized, iss, azp, aud, sub, email, email_verified, at_hash, name, picture, given_name, family_name, 
        locale, iat, exp, login, id, node_id, avatar_url, gravatar_id, url, html_url, followers_url, following_url, 
        gists_url, starred_url, subscriptions_url, organizations_url, repos_url, events_url, received_events_url, type, 
        site_admin, company, blog, location, hireable, bio, twitter_username, public_repos, public_gists, followers, 
        following, created_at, updated_at, context, businessPhones, displayName, givenName, jobTitle, mail, mobilePhone, 
        officeLocation, preferredLanguage, surname, userPrincipalName, self, accountId, emailAddress, avatarUrls, 
        active, timeZone, accountType, account_id, familiar_name, display_name, abbreviated_name, disabled, country, 
        referral_link, team, account_type, root_info, profile_photo_url, membership_type, team_member_id, is_paired, 
        account_migration_state)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        values = (self.session_id, self.request_secret, self.state, self.most_recent_source_route,
                  self.datetime_created, self.in_login, self.provider, self.provider_authorized, self.iss, self.azp,
                  self.aud, self.sub, self.email, self.email_verified, self.at_hash, self.name, self.picture,
                  self.given_name, self.family_name, self.locale, self.iat, self.exp, self.login, self.id, self.node_id,
                  self.avatar_url, self.gravatar_id, self.url, self.html_url, self.followers_url, self.following_url,
                  self.gists_url, self.starred_url, self.subscriptions_url, self.organizations_url, self.repos_url,
                  self.events_url, self.received_events_url, self.type, self.site_admin, self.company, self.blog,
                  self.location, self.hireable, self.bio, self.twitter_username, self.public_repos, self.public_gists,
                  self.followers, self.following, self.created_at, self.updated_at, self.context,
                  pickle.dumps(self.businessPhones), self.displayName, self.givenName, self.jobTitle, self.mail,
                  self.mobilePhone, self.officeLocation, self.preferredLanguage, self.surname, self.userPrincipalName,
                  self.self, self.accountId, self.emailAddress, pickle.dumps(self.avatarUrls), self.active,
                  self.timeZone, self.accountType, self.account_id, self.familiar_name, self.display_name,
                  self.abbreviated_name, self.disabled, self.country, self.referral_link, pickle.dumps(self.team),
                  pickle.dumps(self.account_type), pickle.dumps(self.root_info), self.profile_photo_url,
                  pickle.dumps(self.membership_type), self.team_member_id, self.is_paired,
                  pickle.dumps(self.account_migration_state))
        conn = sqlite3.connect('sessions.db')
        cursor = conn.cursor()
        # Delete any sessions that are older than a week
        one_week_ago = datetime.now() - timedelta(days=7)
        cursor.execute("DELETE FROM sessions WHERE datetime_created < ?", (one_week_ago,))

        cursor.execute(query, values)
        conn.commit()
        conn.close()

    def delete(self):
        # Remove the session from the database
        conn = sqlite3.connect('sessions.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sessions WHERE session_id = ?;', (self.session_id,))
        conn.commit()
        conn.close()

    @classmethod
    def load(cls, session_id):
        # Load a session from the database by session ID
        conn = sqlite3.connect('sessions.db')
        cursor = conn.cursor()
        results = cursor.execute('SELECT * FROM sessions WHERE session_id = ?;', (session_id,))
        row = results.fetchone()
        if row:
            return cls(*row)
        else:
            return None

    def add_id_info(self, provider: str, id_info: dict, provider_authorized: bool):
        self.provider = provider
        self.provider_authorized = provider_authorized
        self.iss = id_info.get("iss", None)
        self.azp = id_info.get("azp", None)
        self.aud = id_info.get("aud", None)
        self.sub = id_info.get("sub", None)
        self.email = id_info.get("email", None)
        self.at_hash = id_info.get("at_hash", None)
        name = id_info.get("name", None)
        if type(name) is dict:
            self.name = None
            self.given_name = name.get("email_verified", False)
            self.surname = name.get("surname", False)
            self.familiar_name = name.get("familiar_name", False)
            self.display_name = name.get("display_name", False)
            self.abbreviated_name = name.get("abbreviated_name", False)
        else:
            self.name = name
            self.given_name = id_info.get("email_verified", False)
            self.surname = id_info.get("surname", False)
            self.familiar_name = id_info.get("familiar_name", False)
            self.display_name = id_info.get("display_name", False)
            self.abbreviated_name = id_info.get("abbreviated_name", False)
        self.picture = id_info.get("picture", None)
        self.family_name = id_info.get("family_name", None)
        self.locale = id_info.get("locale", None)
        self.iat = id_info.get("iat", None)
        self.exp = id_info.get("exp", None)
        self.login = id_info.get("login", None)
        self.id = id_info.get("id", None)
        self.node_id = id_info.get("node_id", None)
        self.avatar_url = id_info.get("avatar_url", None)
        self.gravatar_id = id_info.get("gravatar_id", None)
        self.url = id_info.get("url", None)
        self.html_url = id_info.get("html_url", None)
        self.followers_url = id_info.get("followers_url", None)
        self.following_url = id_info.get("following_url", None)
        self.gists_url = id_info.get("gists_url", None)
        self.starred_url = id_info.get("starred_url", None)
        self.subscriptions_url = id_info.get("subscriptions_url", None)
        self.organizations_url = id_info.get("organizations_url", None)
        self.repos_url = id_info.get("repos_url", None)
        self.events_url = id_info.get("events_url", None)
        self.received_events_url = id_info.get("received_events_url", None)
        self.type = id_info.get("type", None)
        self.site_admin = id_info.get("site_admin", None)
        self.company = id_info.get("company", None)
        self.blog = id_info.get("blog", None)
        self.location = id_info.get("location", None)
        self.hireable = id_info.get("hireable", None)
        self.bio = id_info.get("bio", None)
        self.twitter_username = id_info.get("twitter_username", None)
        self.public_repos = id_info.get("public_repos", None)
        self.public_gists = id_info.get("public_gists", None)
        self.followers = id_info.get("followers", None)
        self.following = id_info.get("following", None)
        self.created_at = id_info.get("created_at", None)
        self.updated_at = id_info.get("updated_at", None)
        self.context = id_info.get("@odata.context", None)
        self.businessPhones = id_info.get("businessPhones", [])
        self.displayName = id_info.get("displayName", None)
        self.givenName = id_info.get("givenName", None)
        self.jobTitle = id_info.get("jobTitle", None)
        self.mail = id_info.get("mail", None)
        self.mobilePhone = id_info.get("mobilePhone", None)
        self.officeLocation = id_info.get("officeLocation", None)
        self.preferredLanguage = id_info.get("preferredLanguage", None)
        self.surname = id_info.get("surname", None)
        self.userPrincipalName = id_info.get("userPrincipalName", None)
        self.self = id_info.get("self", None)
        self.accountId = id_info.get("accountId", None)
        self.emailAddress = id_info.get("emailAddress", None)
        self.avatarUrls = id_info.get("avatarUrls", {})
        self.active = id_info.get("active", False)
        self.timeZone = id_info.get("timeZone", None)
        self.accountType = id_info.get("accountType", None)
        self.disabled = id_info.get("disabled", False)
        self.country = id_info.get("country", None)
        self.referral_link = id_info.get("referral_link", None)
        self.team = id_info.get("team", {})
        self.account_type = id_info.get("account_type", {})
        self.root_info = id_info.get("root_info", {})
        self.profile_photo_url = id_info.get("profile_photo_url", None)
        self.membership_type = id_info.get("membership_type", {})
        self.team_member_id = id_info.get("team_member_id", None)
        self.is_paired = id_info.get("is_paired", None)
        self.account_migration_state = id_info.get("account_migration_state", {})
        self.save()

    def logout(self):
        self.provider = None
        self.provider_authorized = False
        self.iss = None
        self.azp = None
        self.aud = None
        self.sub = None
        self.email = None
        self.email_verified = False
        self.at_hash = None
        self.name = None
        self.picture = None
        self.given_name = None
        self.family_name = None
        self.locale = None
        self.iat = None
        self.exp = None
        self.login = None
        self.id = None
        self.node_id = None
        self.avatar_url = None
        self.gravatar_id = None
        self.url = None
        self.html_url = None
        self.followers_url = None
        self.following_url = None
        self.gists_url = None
        self.starred_url = None
        self.subscriptions_url = None
        self.organizations_url = None
        self.repos_url = None
        self.events_url = None
        self.received_events_url = None
        self.type = None
        self.site_admin = None
        self.company = None
        self.blog = None
        self.location = None
        self.hireable = None
        self.bio = None
        self.twitter_username = None
        self.public_repos = None
        self.public_gists = None
        self.followers = None
        self.following = None
        self.created_at = None
        self.updated_at = None
        self.context = None
        self.businessPhones = []
        self.displayName = None
        self.givenName = None
        self.jobTitle = None
        self.mail = None
        self.mobilePhone = None
        self.officeLocation = None
        self.preferredLanguage = None
        self.surname = None
        self.userPrincipalName = None
        self.self = None
        self.accountId = None
        self.emailAddress = None
        self.avatarUrls = {}
        self.active = False
        self.timeZone = None
        self.accountType = None
        self.account_id = None
        self.familiar_name = None
        self.display_name = None
        self.abbreviated_name = None
        self.disabled = False
        self.country = None
        self.referral_link = None
        self.team = {}
        self.account_type = {}
        self.root_info = {}
        self.profile_photo_url = None
        self.membership_type = {}
        self.team_member_id = None
        self.is_paired = None
        self.account_migration_state = {}
        self.save()

    def set_in_login(self):
        self.in_login = True
        self.save()

    def set_out_login(self):
        self.in_login = False
        self.save()

    def create_new_request_secret(self, length=40):
        self.request_secret = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        self.save()
        return self.request_secret


# Define the Internal Auth User class
class InternalAuthUser:
    def __init__(self, user_id):
        self.user_id = user_id
        conn = sqlite3.connect('internal_auth.db')
        cursor = conn.cursor()
        results = cursor.execute('SELECT * FROM users_auth WHERE user_id = ?;', (self.user_id,))
        row = results.fetchone()
        conn.close()
        if row:
            (
                self.user_id, self.email, self.first_name, self.middle_name, self.last_name, self.client_salt,
                self.server_salt, self.hashed_password, self.user_completed, self.created_at
             ) = row
        else:
            self.email = None
            self.first_name = None
            self.middle_name = None
            self.last_name = None
            self.client_salt = None
            self.server_salt = None
            self.hashed_password = None
            self.user_completed = False
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save()

    def save(self):
        # Save the current state of the user to the database
        query = f'''INSERT OR REPLACE INTO users_auth
        (user_id, email, first_name, middle_name, last_name, client_salt, server_salt, hashed_password, user_completed, 
        created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        values = (self.user_id, self.email, self.first_name, self.middle_name, self.last_name, self.client_salt,
                  self.server_salt, self.hashed_password, self.user_completed, self.created_at)
        conn = sqlite3.connect('internal_auth.db')
        cursor = conn.cursor()

        cursor.execute(query, values)
        conn.commit()
        conn.close()

    def delete(self):
        # Remove the session from the database
        conn = sqlite3.connect('internal_auth.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users_auth WHERE user_id = ?;', (self.user_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def email_exists_and_completed(email):
        conn = sqlite3.connect('internal_auth.db')
        cursor = conn.cursor()
        results = cursor.execute('SELECT * FROM users_auth WHERE email = ? AND user_completed = 1;', (email,))
        row = results.fetchone()
        conn.close()
        return row is not None

    @staticmethod
    def create_user(email):
        conn = sqlite3.connect('internal_auth.db')
        cursor = conn.cursor()

        # Check if the email already exists in the database
        results = cursor.execute('SELECT * FROM users_auth WHERE email = ?;', (email,))
        row = results.fetchone()
        if row:
            conn.close()
            raise ValueError('Email address already exists in database.')

        # Generate a random user ID, client salt, and server salt
        user_id = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        client_salt = ''.join(random.choices(string.ascii_letters + string.digits, k=40))
        server_salt = ''.join(random.choices(string.ascii_letters + string.digits, k=40))

        # Insert the new user into the database
        query = '''INSERT INTO users_auth 
            (user_id, email, client_salt, server_salt, user_completed, created_at) 
            VALUES (?, ?, ?, ?, ?, ?);'''
        values = (user_id, email, client_salt, server_salt, False, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cursor.execute(query, values)
        conn.commit()
        conn.close()

        # Return a new instance of InternalAuthUser for the newly created user
        return InternalAuthUser(user_id)

    @staticmethod
    def get_user_by_email(email):
        conn = sqlite3.connect('internal_auth.db')
        cursor = conn.cursor()

        # Retrieve the user record from the database
        results = cursor.execute('SELECT * FROM users_auth WHERE email = ?;', (email,))
        row = results.fetchone()

        # If no user with the given email exists, return None
        if not row:
            conn.close()
            return None

        # Otherwise, create and return an instance of InternalAuthUser for the retrieved user
        user_id = row[0]
        conn.close()
        return InternalAuthUser(user_id)

    def update_user_info(self, first_name, middle_name, last_name, password):
        if self.user_completed:
            raise ValueError('User information already completed.')

        # Concatenate the hashed password with the server salt and hash it using sha256
        salted_password = self.server_salt + password
        hashed_password = argon2.hash(salted_password)

        # Update the user properties
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.hashed_password = hashed_password
        self.user_completed = True
        self.save()

    def check_password(self, password):
        # Salt the provided password with the server salt and hash it using sha256
        salted_password = self.server_salt + password

        # Check if the hashed password matches the one on record
        return argon2.verify(salted_password, self.hashed_password)
