import sqlite3

DATABASE = 'database.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY,
            ip TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            city TEXT,
            state TEXT,
            country TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized.")
