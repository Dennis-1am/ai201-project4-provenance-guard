UPDATE_CONTENT_STATUS = '''
    UPDATE content_labels
    SET status = ?, appeal_reasoning = ?
    WHERE content_id = ?
'''

INSERT_APPEAL_LOG = '''
    INSERT INTO logs (
        content_id, timestamp, heuristic_score,
        groq_score, final_score, status, appeal_reasoning, action_taken
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
'''
