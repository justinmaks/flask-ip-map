from flask import Flask, request, render_template, g
import sqlite3
import requests
import os
import logging

app = Flask(__name__)

DATABASE = 'database.db'
IPINFO_TOKEN = os.getenv('IPINFO_TOKEN')  # Ensure you set this environment variable

# Set up logging
logging.basicConfig(level=logging.INFO)

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

def get_client_ip():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    elif request.headers.get("CF-Connecting-IP"):
        ip = request.headers.get("CF-Connecting-IP")
    else:
        ip = request.remote_addr
    return ip

def get_geo_data(ip):
    response = requests.get(f"https://ipinfo.io/{ip}?token={IPINFO_TOKEN}")
    app.logger.info(f"IP API response status: {response.status_code}")
    app.logger.info(f"IP API response data: {response.text}")
    response.raise_for_status()  # Raise an HTTPError for bad responses
    return response.json()

@app.route('/')
def index():
    ip = get_client_ip()
    try:
        geo_data = get_geo_data(ip)
        app.logger.info(f"Geo data: {geo_data}")
        latitude, longitude = map(float, geo_data['loc'].split(','))
    except KeyError:
        app.logger.error(f"Geo data for IP {ip} does not contain 'loc' key: {geo_data}")
        latitude, longitude = 0.0, 0.0  # Default values or handle as needed
    except requests.RequestException as e:
        app.logger.error(f"RequestException for IP {ip}: {e}")
        latitude, longitude = 0.0, 0.0  # Default values or handle as needed

    db = get_db()
    db.execute('INSERT INTO visits (ip, latitude, longitude) VALUES (?, ?, ?)', [ip, latitude, longitude])
    db.commit()

    visits = query_db('SELECT latitude, longitude FROM visits')

    return render_template('map.html', visits=visits)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
