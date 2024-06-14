import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''
          CREATE TABLE visits
          (id INTEGER PRIMARY KEY, ip TEXT, latitude REAL, longitude REAL)
          ''')
conn.commit()
conn.close()
