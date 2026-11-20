
import sqlite3
import pandas as pd

# Connect to the RUM database
conn = sqlite3.connect("data/rum.db")

# Load events into a Pandas DataFrame
df = pd.read_sql_query(
    "SELECT * FROM rum_events",
    conn
)

conn.close()

# Display the collected events
print("\n--- RUM EVENTS ---")
print(df[["id", "event_name", "page_name", "timestamp"]])

# Count each event type
print("\n--- EVENT SUMMARY ---")
print(df["event_name"].value_counts())

# Count feature usage
print("\n--- FEATURE USAGE ---")
print(
    df[df["event_name"] == "feature_used"]
    ["page_name"]
    .value_counts()
)


# Convert timestamps into datetime objects
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

# Select task start and completion events
starts = df[df["event_name"] == "task_started"].copy()
completions = df[df["event_name"] == "task_completed"].copy()

# Number repeated tasks within each session
group_columns = ["session_id", "task_id"]

starts["task_number"] = starts.groupby(group_columns).cumcount()
completions["task_number"] = completions.groupby(group_columns).cumcount()

# Match each start with its corresponding completion
tasks = starts.merge(
    completions,
    on=group_columns + ["task_number"],
    suffixes=("_start", "_complete")
)

# Calculate elapsed task duration
tasks["duration_seconds"] = (
    tasks["timestamp_complete"] - tasks["timestamp_start"]
).dt.total_seconds()

print("\n--- TASK COMPLETION ANALYSIS ---")
print(tasks[[
    "task_id",
    "task_number",
    "duration_seconds"
]])

print("\nAverage task duration:")
print(tasks["duration_seconds"].mean(), "seconds")

