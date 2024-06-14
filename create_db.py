import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Check if the visits table exists
c.execute('''
    SELECT name FROM sqlite_master WHERE type='table' AND name='visits';
''')

table_exists = c.fetchone()

# If the visits table does not exist, create it
if not table_exists:
    c.execute('''
        CREATE TABLE visits
        (id INTEGER PRIMARY KEY, ip TEXT, latitude REAL, longitude REAL)
    ''')

conn.commit()
conn.close()
