
from flask import Flask, render_template, request, jsonify
import sqlite3
import json
from datetime import datetime, timezone

app = Flask(__name__)

DB_PATH = "data/rum.db"


def initialize_database():
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS rum_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_id TEXT,
            event_name TEXT,
            page_name TEXT,
            task_id TEXT,
            action_description TEXT,
            timestamp TEXT,
            metadata TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'OPEN',
            created_at TEXT
        )
    """)


    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/events", methods=["POST"])
def collect_event():

    event = request.get_json()

    required_fields = [
        "session_id",
        "event_name",
        "page_name",
        "timestamp"
    ]

    if not event or any(
        not event.get(field) for field in required_fields
    ):
        return jsonify({"error": "Missing required fields"}), 400

    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        INSERT INTO rum_events (
            session_id,
            user_id,
            event_name,
            page_name,
            task_id,
            action_description,
            timestamp,
            metadata
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event["session_id"],
        event.get("user_id", "anonymous"),
        event["event_name"],
        event["page_name"],
        event.get("task_id"),
        event.get("action_description"),
        event["timestamp"],
        json.dumps(event.get("metadata", {}))
    ))

    conn.commit()
    conn.close()

    return jsonify({"status": "event recorded"}), 201



@app.route("/api/tickets", methods=["POST"])
def create_ticket():

    ticket = request.get_json()

    # Validate ticket description
    if not ticket or not ticket.get("description", "").strip():
        return jsonify({"error": "Description is required"}), 400

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.execute("""
        INSERT INTO tickets (user_id, description, created_at)
        VALUES (?, ?, ?)
    """, (
        ticket.get("user_id", "anonymous"),
        ticket["description"].strip(),
        datetime.now(timezone.utc).isoformat()
    ))

    ticket_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Ticket created successfully",
        "ticket_id": ticket_id,
        "status": "OPEN"
    }), 201



@app.route("/api/events", methods=["GET"])
def get_events():

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT * FROM rum_events
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


@app.route("/api/dashboard/summary", methods=["GET"])
def dashboard_summary():

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Average service availability
    availability = conn.execute("""
        SELECT ROUND(AVG(availability), 2)
        FROM services
    """).fetchone()[0]

    # Count active incidents
    active_incidents = conn.execute("""
        SELECT COUNT(*)
        FROM incidents
        WHERE status != 'Resolved'
    """).fetchone()[0]

    # Count all support tickets
    total_tickets = conn.execute("""
        SELECT COUNT(*)
        FROM tickets
    """).fetchone()[0]

    # Count unique user sessions
    user_sessions = conn.execute("""
        SELECT COUNT(DISTINCT session_id)
        FROM rum_events
    """).fetchone()[0]

    conn.close()

    return jsonify({
        "service_availability": availability or 0,
        "active_incidents": active_incidents,
        "total_tickets": total_tickets,
        "user_sessions": user_sessions
    })


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True, port=5000)
