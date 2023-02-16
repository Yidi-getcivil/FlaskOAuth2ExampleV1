import os


class Config(object):
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY") or "yidissupersecretkey"
    SQLITE3_DATABASE_URI = os.environ.get("DATABASE_URL") or "sessions.db"
    GITHUB_OAUTH_CLIENT_ID = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
    GITHUB_OAUTH_CLIENT_SECRET = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
    GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    AZURE_OAUTH_CLIENT_ID = os.environ.get("AZURE_OAUTH_CLIENT_ID")
    AZURE_OAUTH_CLIENT_SECRET = os.environ.get("AZURE_OAUTH_CLIENT_SECRET")
