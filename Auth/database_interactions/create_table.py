import sqlite3


def create_sessions_table():
    # Create a connection to the database
    conn = sqlite3.connect('sessions.db')
    cursor = conn.cursor()

    # Create the sessions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
      session_id TEXT PRIMARY KEY,
      request_secret TEXT,
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
      updated_at TEXT,
      context TEXT,
      businessPhones BLOB,
      displayName TEXT,
      givenName TEXT,
      jobTitle TEXT,
      mail TEXT,
      mobilePhone TEXT,
      officeLocation TEXT,
      preferredLanguage TEXT,
      surname TEXT,
      userPrincipalName TEXT,
      self TEXT,
      accountId TEXT,
      emailAddress TEXT,
      avatarUrls BLOB,
      active BOOLEAN,
      timeZone TEXT,
      accountType TEXT,
      account_id TEXT,
      familiar_name TEXT,
      display_name TEXT,
      abbreviated_name TEXT,
      disabled BOOLEAN,
      country TEXT,
      referral_link TEXT,
      team BLOB,
      account_type BLOB,
      root_info BLOB,
      profile_photo_url TEXT,
      membership_type BLOB,
      team_member_id TEXT,
      is_paired BOOLEAN,
      account_migration_state BLOB
    );
    ''')
    conn.commit()

    conn.close()


def create_users_auth_table():
    # Create a connection to the database
    conn = sqlite3.connect('internal_auth.db')
    cursor = conn.cursor()

    # Create the sessions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users_auth (
      user_id TEXT PRIMARY KEY,
      email TEXT,
      first_name TEXT,
      middle_name TEXT,
      last_name TEXT,
      client_salt TEXT,
      server_salt TEXT,
      hashed_password TEXT,
      user_completed BOOLEAN,
      created_at TEXT
    );
    ''')
    conn.commit()

    conn.close()
