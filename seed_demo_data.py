
import sqlite3
import random
import json
from datetime import datetime, timedelta, timezone

DB_PATH = "data/rum.db"
rng = random.Random(42)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 1. Create services table
cursor.execute("""
CREATE TABLE IF NOT EXISTS services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    status TEXT,
    availability REAL,
    response_time_ms INTEGER,
    source TEXT DEFAULT 'demo_seed'
)
""")

# 2. Create incidents table
cursor.execute("""
CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    service_name TEXT,
    severity TEXT,
    status TEXT,
    description TEXT,
    created_at TEXT,
    source TEXT DEFAULT 'demo_seed'
)
""")

# Remove previous synthetic records so the script is repeatable
cursor.execute("DELETE FROM services WHERE source = 'demo_seed'")
cursor.execute("DELETE FROM incidents WHERE source = 'demo_seed'")
cursor.execute("DELETE FROM tickets WHERE user_id = 'demo_seed'")

cursor.execute("""
DELETE FROM rum_events
WHERE metadata LIKE '%demo_seed%'
""")

# 3. Generate cloud services
services = [
    ("API Gateway", "Networking", "Healthy", 99.99, 125),
    ("Authentication Service", "Security", "Healthy", 99.98, 95),
    ("Customer Database", "Database", "Degraded", 98.70, 840),
    ("Payment Service", "Application", "Healthy", 99.95, 210),
    ("Notification Service", "Application", "Healthy", 99.90, 180),
    ("Monitoring Service", "Observability", "Healthy", 99.99, 110),
    ("Storage Service", "Storage", "Healthy", 99.97, 145),
    ("Cloud Scheduler", "Infrastructure", "Maintenance", 99.80, 320)
]

cursor.executemany("""
INSERT INTO services
(name, category, status, availability, response_time_ms, source)
VALUES (?, ?, ?, ?, ?, 'demo_seed')
""", services)

# 4. Generate incidents
now = datetime.now(timezone.utc)

incident_data = [
    ("Database response latency", "Customer Database", "High",
     "Investigating", "Database response time exceeded the expected threshold."),
    ("Payment API intermittent errors", "Payment Service", "Critical",
     "Open", "Elevated HTTP 5xx responses detected."),
    ("Authentication timeout", "Authentication Service", "Medium",
     "Resolved", "Temporary authentication delay observed."),
    ("Storage request latency", "Storage Service", "Low",
     "Resolved", "Short increase in storage request latency."),
    ("Notification delivery delay", "Notification Service", "Medium",
     "Open", "Delayed delivery of application notifications."),
    ("API gateway traffic spike", "API Gateway", "High",
     "Monitoring", "Unexpected increase in incoming requests.")
]

for i, incident in enumerate(incident_data):
    title, service, severity, status, description = incident

    created = now - timedelta(hours=(i + 2) * 5)

    cursor.execute("""
        INSERT INTO incidents
        (title, service_name, severity, status, description,
         created_at, source)
        VALUES (?, ?, ?, ?, ?, ?, 'demo_seed')
    """, (
        title, service, severity, status,
        description, created.isoformat()
    ))

# 5. Generate synthetic support tickets
ticket_descriptions = [
    "Unable to access cloud dashboard",
    "API response time is unusually high",
    "Authentication request failed",
    "Database connection timeout",
    "Storage upload is taking too long",
    "Notification service is not responding",
    "Unable to view service health metrics",
    "Deployment status is not updating"
]

for i in range(30):
    created = now - timedelta(days=rng.randint(0, 6),
                              hours=rng.randint(0, 23))

    status = rng.choices(
        ["OPEN", "IN_PROGRESS", "RESOLVED"],
        weights=[20, 25, 55]
    )[0]

    cursor.execute("""
        INSERT INTO tickets
        (user_id, description, status, created_at)
        VALUES (?, ?, ?, ?)
    """, (
        "demo_seed",
        rng.choice(ticket_descriptions),
        status,
        created.isoformat()
    ))

# 6. Generate synthetic RUM events
features = [
    "service_dashboard",
    "incident_management",
    "support_tickets",
    "user_analytics"
]

for session_number in range(1, 31):

    session_id = f"demo-session-{session_number:03d}"

    session_start = now - timedelta(
        days=rng.randint(0, 6),
        hours=rng.randint(0, 23)
    )

    events = [
        (
            "page_view",
            "home",
            None,
            "User opened CloudOps portal"
        ),
        (
            "feature_used",
            rng.choice(features),
            None,
            "User accessed an application feature"
        ),
        (
            "task_started",
            "support_tickets",
            "ticket_creation",
            "User started creating a support ticket"
        )
    ]

    # Most sessions complete the task; some fail
    outcome = rng.choices(
        ["task_completed", "task_failed"],
        weights=[85, 15]
    )[0]

    events.append((
        outcome,
        "support_tickets",
        "ticket_creation",
        "Support ticket workflow outcome"
    ))

    for event_number, event in enumerate(events):
        event_name, page_name, task_id, description = event

        event_time = session_start + timedelta(
            seconds=event_number * rng.randint(20, 90)
        )

        metadata = {
            "source": "demo_seed",
            "synthetic": True
        }

        cursor.execute("""
            INSERT INTO rum_events
            (session_id, user_id, event_name, page_name,
             task_id, action_description, timestamp, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            f"demo_user_{rng.randint(1, 50):03d}",
            event_name,
            page_name,
            task_id,
            description,
            event_time.isoformat(),
            json.dumps(metadata)
        ))

conn.commit()

print("Synthetic demo data generated successfully!")
print("Services:", cursor.execute(
    "SELECT COUNT(*) FROM services WHERE source='demo_seed'"
).fetchone()[0])

print("Incidents:", cursor.execute(
    "SELECT COUNT(*) FROM incidents WHERE source='demo_seed'"
).fetchone()[0])

print("Demo tickets:", cursor.execute(
    "SELECT COUNT(*) FROM tickets WHERE user_id='demo_seed'"
).fetchone()[0])

print("Demo RUM events:", cursor.execute(
    "SELECT COUNT(*) FROM rum_events WHERE metadata LIKE '%demo_seed%'"
).fetchone()[0])

conn.close()
