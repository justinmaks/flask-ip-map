import sqlite3

DATABASE = 'database.db'

def insert_test_data():
    test_data = [
        ('192.168.1.1', 37.7749, -122.4194),
        ('192.168.1.2', 34.0522, -118.2437),
        ('192.168.1.3', 40.7128, -74.0060)
    ]

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.executemany('INSERT INTO visits (ip, latitude, longitude) VALUES (?, ?, ?)', test_data)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    insert_test_data()
    print("Test data inserted.")
