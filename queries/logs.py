GET_RECENT_LOGS = '''
    SELECT l.*, cl.label, cl.appeal_reasoning, cl.creator_id
    FROM logs l
    JOIN content_labels cl ON l.content_id = cl.content_id
    ORDER BY l.timestamp DESC
    LIMIT 3
'''

GET_LOG_BY_CONTENT_ID = '''
    SELECT l.*, cl.label, cl.appeal_reasoning, cl.creator_id
    FROM logs l
    JOIN content_labels cl ON l.content_id = cl.content_id
    WHERE l.content_id = ?
    ORDER BY l.timestamp DESC
    LIMIT 1
'''