# Create a connection to the database
import sqlite3
from datetime import datetime, timedelta
from Auth.database_interactions import create_table

create_table.create_sessions_table()


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
                self.session_id, self.state, self.most_recent_source_route, self.datetime_created, self.in_login,
                self.provider, self.provider_authorized, self.iss, self.azp, self.aud, self.sub, self.email,
                self.email_verified, self.at_hash, self.name, self.picture, self.given_name, self.family_name,
                self.locale, self.iat, self.exp, self.login, self.id, self.node_id, self.avatar_url, self.gravatar_id,
                self.url, self.html_url, self.followers_url, self.following_url, self.gists_url, self.starred_url,
                self.subscriptions_url, self.organizations_url, self.repos_url, self.events_url,
                self.received_events_url, self.type, self.site_admin, self.company, self.blog, self.location,
                self.hireable, self.bio, self.twitter_username, self.public_repos, self.public_gists, self.followers,
                self.following, self.created_at, self.updated_at
             ) = row
        else:
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
        self.save()

    def save(self):
        # Save the current state of the session to the database
        query = f'''INSERT OR REPLACE INTO sessions 
        (session_id, state, most_recent_source_route, datetime_created, in_login, provider, provider_authorized, iss, 
        azp, aud, sub, email, email_verified, at_hash, name, picture, given_name, family_name, locale, iat, exp, login, 
        id, node_id, avatar_url, gravatar_id, url, html_url, followers_url, following_url, gists_url, starred_url, 
        subscriptions_url, organizations_url, repos_url, events_url, received_events_url, type, site_admin, company, 
        blog, location, hireable, bio, twitter_username, public_repos, public_gists, followers, following, created_at, 
        updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        values = (self.session_id, self.state, self.most_recent_source_route, self.datetime_created, self.in_login,
                  self.provider, self.provider_authorized, self.iss, self.azp, self.aud, self.sub, self.email,
                  self.email_verified, self.at_hash, self.name, self.picture, self.given_name, self.family_name,
                  self.locale, self.iat, self.exp, self.login, self.id, self.node_id, self.avatar_url, self.gravatar_id,
                  self.url, self.html_url, self.followers_url, self.following_url, self.gists_url, self.starred_url,
                  self.subscriptions_url, self.organizations_url, self.repos_url, self.events_url,
                  self.received_events_url, self.type, self.site_admin, self.company, self.blog, self.location,
                  self.hireable, self.bio, self.twitter_username, self.public_repos, self.public_gists, self.followers,
                  self.following, self.created_at, self.updated_at)
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
        self.email_verified = id_info.get("email_verified", False)
        self.at_hash = id_info.get("at_hash", None)
        self.name = id_info.get("name", None)
        self.picture = id_info.get("picture", None)
        self.given_name = id_info.get("given_name", None)
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
        self.save()

    def set_in_login(self):
        self.in_login = True
        self.save()

    def set_out_login(self):
        self.in_login = False
        self.save()
