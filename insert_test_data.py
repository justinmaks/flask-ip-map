import sqlite3

DATABASE = 'database.db'

def insert_test_data():
    test_data = [
        ('192.168.1.1', 37.7749, -122.4194, 'San Francisco', 'California', 'USA'),
        ('192.168.1.2', 34.0522, -118.2437, 'Los Angeles', 'California', 'USA'),
        ('192.168.1.3', 40.7128, -74.0060, 'New York', 'New York', 'USA'),
        ('203.0.113.1', 48.8566, 2.3522, 'Paris', 'Île-de-France', 'France'),
        ('203.0.113.2', 51.5074, -0.1278, 'London', 'England', 'United Kingdom'),
        ('203.0.113.3', 52.5200, 13.4050, 'Berlin', 'Berlin', 'Germany'),
        ('203.0.113.4', 40.4168, -3.7038, 'Madrid', 'Community of Madrid', 'Spain'),
        ('203.0.113.5', 41.9028, 12.4964, 'Rome', 'Lazio', 'Italy')
    ]

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.executemany('INSERT INTO visits (ip, latitude, longitude, city, state, country) VALUES (?, ?, ?, ?, ?, ?)', test_data)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    insert_test_data()
    print("Test data inserted.")
