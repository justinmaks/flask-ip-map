from flask import Flask, request, render_template, g
import sqlite3
import requests
import os
import logging
import matplotlib.pyplot as plt

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
        ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
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

def get_country_statistics():
    stats = query_db('SELECT country, COUNT(DISTINCT ip) as count FROM visits GROUP BY country ORDER BY count DESC')
    return stats

def generate_country_chart(stats):
    countries = [stat[0] for stat in stats]
    counts = [stat[1] for stat in stats]

    plt.figure(figsize=(10, 6))
    plt.bar(countries, counts, color='skyblue')
    plt.xlabel('Country')
    plt.ylabel('Number of Visitors')
    plt.title('Number of Visitors by Country')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    if not os.path.exists('static'):
        os.makedirs('static')
    
    chart_path = os.path.join('static', 'country_chart.png')
    plt.savefig(chart_path)
    plt.close()
    return chart_path

@app.route('/')
def index():
    ip = get_client_ip()
    try:
        geo_data = get_geo_data(ip)
        app.logger.info(f"Geo data: {geo_data}")
        latitude, longitude = map(float, geo_data['loc'].split(','))
        city = geo_data.get('city', 'Unknown')
        state = geo_data.get('region', 'Unknown')
        country = geo_data.get('country', 'Unknown')
    except KeyError:
        app.logger.error(f"Geo data for IP {ip} does not contain 'loc' key: {geo_data}")
        latitude, longitude = 0.0, 0.0  # Default values or handle as needed
        city = state = country = 'Unknown'
    except requests.RequestException as e:
        app.logger.error(f"RequestException for IP {ip}: {e}")
        latitude, longitude = 0.0, 0.0  # Default values or handle as needed
        city = state = country = 'Unknown'

    db = get_db()
    db.execute('INSERT INTO visits (ip, latitude, longitude, city, state, country) VALUES (?, ?, ?, ?, ?, ?)',
               [ip, latitude, longitude, city, state, country])
    db.commit()

    visits = query_db('SELECT ip, latitude, longitude, city, state, country FROM visits')
    unique_ips_count = query_db('SELECT COUNT(DISTINCT ip) FROM visits', one=True)[0]
    country_stats = get_country_statistics()
    chart_path = generate_country_chart(country_stats)

    return render_template('map.html', visits=visits, unique_ips_count=unique_ips_count, country_stats=country_stats, chart_path=chart_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
