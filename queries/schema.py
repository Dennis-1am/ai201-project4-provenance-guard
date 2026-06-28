CREATE_CONTENT_TABLE = '''
    CREATE TABLE IF NOT EXISTS content (
        content_id TEXT PRIMARY KEY,
        creator_id TEXT,
        text_body TEXT
    )
'''

CREATE_LABELS_TABLE = '''
    CREATE TABLE IF NOT EXISTS content_labels (
        content_id TEXT PRIMARY KEY,
        creator_id TEXT,
        confidence_score REAL,
        label TEXT,
        status TEXT,
        appeal_reasoning TEXT,
        FOREIGN KEY (content_id) REFERENCES content (content_id)
    )
'''

CREATE_LOGS_TABLE = '''
    CREATE TABLE IF NOT EXISTS logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        content_id TEXT,
        timestamp TEXT,
        heuristic_score REAL,
        groq_score REAL,
        final_score REAL,
        status TEXT,
        appeal_reasoning TEXT,
        action_taken TEXT,
        FOREIGN KEY (content_id) REFERENCES content (content_id)
    )
'''