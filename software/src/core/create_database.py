import sqlite3


# Create logs table
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_address TEXT NOT NULL,
    threat_level TEXT NOT NULL,
    action TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# Insert a log entry
cursor.execute("""
INSERT INTO logs (ip_address, threat_level, action)
VALUES (?, ?, ?)
""", ("192.168.1.100", "high", "blocked"))
conn.commit()

# Fetch and display logs
cursor.execute("SELECT * FROM logs")
logs = cursor.fetchall()
for log in logs:
    print(log)

# Close connection
conn.close()