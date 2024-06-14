from flask import Flask, request, render_template, g
import sqlite3
import requests

app = Flask(__name__)

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    ip = request.remote_addr
    geo_url = f"https://freegeoip.app/json/{ip}"
    geo_data = requests.get(geo_url).json()
    latitude = geo_data['latitude']
    longitude = geo_data['longitude']

    db = get_db()
    db.execute('INSERT INTO visits (ip, latitude, longitude) VALUES (?, ?, ?)', [ip, latitude, longitude])
    db.commit()

    visits = query_db('SELECT latitude, longitude FROM visits')

    return render_template('map.html', visits=visits)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
