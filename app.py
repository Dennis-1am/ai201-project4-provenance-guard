from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3
import uuid
import datetime

# Import your heuristic engine 


# Import SQL queries
from llm import llm_evaluator_engine
from queries.schema import CREATE_CONTENT_TABLE, CREATE_LABELS_TABLE, CREATE_LOGS_TABLE
from queries.submission import INSERT_CONTENT, INSERT_LABEL, INSERT_LOG
from queries.logs import GET_RECENT_LOGS
from scoring_engine import score_text, get_status_label

app = Flask(__name__)

# Updated Database Name
DB_NAME = "provenance_guard.db"

# ---------------------------------------------------------
# DATABASE SETUP
# ---------------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute(CREATE_CONTENT_TABLE)
    cursor.execute(CREATE_LABELS_TABLE)
    cursor.execute(CREATE_LOGS_TABLE)
    
    conn.commit()
    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------------------------------------------
# ROUTES
# ---------------------------------------------------------
@app.route('/submit', methods=['POST'])
def submit_endpoint():
    data = request.get_json()
    
    if not data or 'text' not in data or 'creator_id' not in data:
        return jsonify({"error": "Invalid payload. 'text' and 'creator_id' are required."}), 400
        
    ## parse incoming data
    text = data['text']
    creator_id = data['creator_id']

    heuristic_score, groq_score, confidence = score_text(text)
    response = get_status_label(confidence)
    label = response["label"]
    status = response["status"]

    content_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute the imported submission queries
    cursor.execute(INSERT_CONTENT, (content_id, creator_id, text))
    cursor.execute(INSERT_LABEL, (content_id, creator_id, confidence, label, status, None))
    cursor.execute(INSERT_LOG, (
        content_id, timestamp, heuristic_score, 
        groq_score, confidence, f"Initial evaluation compiled label: {label}"
    ))
    
    conn.commit()
    conn.close()
    
    response = {
        "content_id": content_id,
        "attribution": creator_id,
        "confidence": confidence,
        "label": label,
        "status": status
    }
    
    return jsonify(response), 200

@app.route('/log', methods=['GET'])
def get_logs_endpoint():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute the imported log query
    cursor.execute(GET_RECENT_LOGS)
    rows = cursor.fetchall()
    conn.close()
    
    entries = []
    for row in rows:
        entries.append({
            "timestamp": row["timestamp"],
            "content_id": row["content_id"],
            "creator_id": row["creator_id"],
            "scores": {
                "heuristic": row["heuristic_score"],
                "groq_llm": row["groq_score"],
                "final": row["final_score"]
            },
            "label": row["label"],
            "status": row["status"],
            "appeal": row["appeal_text"]
        })
        
    return jsonify({"entries": entries}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)