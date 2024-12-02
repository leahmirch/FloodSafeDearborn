from flask import Flask, render_template, request, redirect, session, url_for, flash
from auth import register_user, authenticate_user
from database import get_connection
import os
from flask import Flask, send_from_directory
from datetime import datetime, timedelta
import json

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.secret_key = 'secretkey'
UPLOAD_FOLDER = '../frontend/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        success, message = register_user(username, email, password)
        
        flash(message)
        if success:
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        success, user = authenticate_user(email, password)
        if success:
            session['user_id'] = user['id']
            return redirect(url_for('home'))
        else:
            flash(user) 
    return render_template('login.html')

@app.route('/home')
def home():
    if 'user_id' not in session:
        flash("You must be logged in to view the flood map!", "error")
        return redirect(url_for('login'))

    conn = get_connection()
    user = conn.execute("SELECT username FROM users WHERE id = ?", (session['user_id'],)).fetchone()
    if not user:
        flash("User not found!", "error")
        return redirect(url_for('login'))

    return render_template('home.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/safety_tips')
def safety_tips():
    return render_template('safety_tips.html')

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join('..', 'backend', 'map'), filename)

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    search_results = []

    content = {
        'Home': 'Welcome to FloodSafeDearborn. Stay informed about flooding.',
        'Resources': 'Find emergency resources and flood preparedness tips.',
        'Contact': 'Reach out to us for more information.',
        'About': 'Learn about FloodSafeDearborn and our mission.',
        'Safety Tips': 'Discover essential flood safety tips.'
    }

    for page, text in content.items():
        if query in text.lower():
            search_results.append(page)

    return render_template('search_results.html', query=query, results=search_results)

@app.route('/submit_event', methods=['GET', 'POST'])
def submit_event():
    if request.method == 'GET':
        return render_template('submit_event.html')

    if request.method == 'POST':
        if 'user_id' not in session:
            flash("You must be logged in to submit an event.", "error")
            return redirect(url_for('login'))

        user_id = session['user_id']
        event_type = request.form.get('event_type')
        duration = int(request.form.get('duration'))
        street = request.form.get('street', '')
        city = request.form.get('city', '')
        state = request.form.get('state', '')
        zip_code = request.form.get('zip', '')
        latitude = request.form.get('latitude', '')
        longitude = request.form.get('longitude', '')

        conn = get_connection()
        with conn:
            cursor = conn.execute("""
                INSERT INTO events (user_id, type, street, city, state, zip, latitude, longitude, duration)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, event_type, street, city, state, zip_code, latitude, longitude, duration))
            event_id = cursor.lastrowid

            if event_type == 'water_levels':
                level = request.form.get('level')
                conn.execute("INSERT INTO water_levels (event_id, level) VALUES (?, ?)", (event_id, level))
            elif event_type == 'flood_severity':
                severity = request.form.get('severity')
                conn.execute("INSERT INTO flood_severity (event_id, severity) VALUES (?, ?)", (event_id, severity))
            elif event_type == 'closed_roads':
                road_name = request.form.get('road_name')
                conn.execute("INSERT INTO closed_roads (event_id, road_name) VALUES (?, ?)", (event_id, road_name))
            elif event_type == 'flood_reports':
                risk = request.form.get('risk')
                conn.execute("INSERT INTO flood_reports (event_id, risk) VALUES (?, ?)", (event_id, risk))
            elif event_type == 'traffic_conditions':
                traffic_level = request.form.get('traffic_level')
                traffic_span = request.form.get('traffic_span')
                conn.execute("INSERT INTO traffic_conditions (event_id, description) VALUES (?, ?)", (event_id, f"{traffic_level}: {traffic_span}"))

        flash("Event submitted successfully!", "success")
        return redirect(url_for('home'))

@app.route('/api/events')
def get_events():
    conn = get_connection()
    query = """
        SELECT events.type, events.latitude, events.longitude, events.street, events.city, events.state, events.zip, 
               events.time, events.duration,
               CASE
                   WHEN events.type = 'water_levels' THEN (SELECT level FROM water_levels WHERE water_levels.event_id = events.id)
                   WHEN events.type = 'flood_severity' THEN (SELECT severity FROM flood_severity WHERE flood_severity.event_id = events.id)
                   WHEN events.type = 'closed_roads' THEN (SELECT road_name FROM closed_roads WHERE closed_roads.event_id = events.id)
                   WHEN events.type = 'flood_reports' THEN (SELECT risk FROM flood_reports WHERE flood_reports.event_id = events.id)
                   WHEN events.type = 'traffic_conditions' THEN (SELECT description FROM traffic_conditions WHERE traffic_conditions.event_id = events.id)
               END AS info
        FROM events
    """
    events = conn.execute(query).fetchall()
    return {"events": [dict(event) for event in events]}

if __name__ == '__main__':
    app.run(debug=True)
