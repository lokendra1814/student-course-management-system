import sqlite3

# Use scms.db instead of cms.db
conn = sqlite3.connect("scms.db")
cursor = conn.cursor()

# Read schema.sql file
with open("schema.sql", "r") as f:
    schema = f.read()

# Execute schema
cursor.executescript(schema)

conn.commit()
conn.close()

print("✅ Database 'scms.db' initialized successfully using schema.sql")