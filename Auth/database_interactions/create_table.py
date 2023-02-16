import sqlite3


def create_sessions_table():
    # Create a connection to the database
    conn = sqlite3.connect('sessions.db')
    cursor = conn.cursor()

    # Create the sessions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
      session_id TEXT PRIMARY KEY,
      state TEXT,
      most_recent_source_route TEXT,
      datetime_created TEXT DEFAULT CURRENT_TIMESTAMP,
      in_login BOOLEAN,
      provider TEXT,
      provider_authorized BOOLEAN,
      iss TEXT,
      azp TEXT,
      aud TEXT,
      sub TEXT,
      email TEXT,
      email_verified BOOLEAN,
      at_hash TEXT,
      name TEXT,
      picture TEXT,
      given_name TEXT,
      family_name TEXT,
      locale TEXT,
      iat TEXT,
      exp TEXT,
      login TEXT,
      id TEXT,
      node_id TEXT,
      avatar_url TEXT,
      gravatar_id TEXT,
      url TEXT,
      html_url TEXT,
      followers_url TEXT,
      following_url TEXT,
      gists_url TEXT,
      starred_url TEXT,
      subscriptions_url TEXT,
      organizations_url TEXT,
      repos_url TEXT,
      events_url TEXT,
      received_events_url TEXT,
      type TEXT,
      site_admin TEXT,
      company TEXT,
      blog TEXT,
      location TEXT,
      hireable TEXT,
      bio TEXT,
      twitter_username TEXT,
      public_repos INTEGER,
      public_gists INTEGER,
      followers INTEGER,
      following INTEGER,
      created_at TEXT,
      updated_at TEXT
    );
    ''')
    conn.commit()

    conn.close()
