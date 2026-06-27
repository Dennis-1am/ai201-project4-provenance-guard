INSERT_CONTENT = '''
    INSERT INTO content (content_id, creator_id, text_body) 
    VALUES (?, ?, ?)
'''

INSERT_LABEL = '''
    INSERT INTO content_labels (content_id, creator_id, confidence_score, label, status, appeal_text)
    VALUES (?, ?, ?, ?, ?, ?)
'''

INSERT_LOG = '''
    INSERT INTO logs (
        content_id, timestamp, heuristic_score, 
        groq_score, final_score, action_taken
    ) VALUES (?, ?, ?, ?, ?, ?)
'''