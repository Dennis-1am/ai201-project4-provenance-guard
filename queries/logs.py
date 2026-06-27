GET_RECENT_LOGS = '''
    SELECT l.*, cl.label, cl.status, cl.appeal_text, cl.creator_id
    FROM logs l
    JOIN content_labels cl ON l.content_id = cl.content_id
    ORDER BY l.timestamp DESC
    LIMIT 3
'''