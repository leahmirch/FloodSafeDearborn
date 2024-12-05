from flask import Flask, render_template, request, redirect, session, url_for, flash
from auth import register_user, authenticate_user
from database import get_connection
import os
from flask import Flask, send_from_directory
from datetime import datetime, timedelta
import json
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import imghdr

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.secret_key = 'secretkey'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'frontend/static/uploads')
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
        
        if success:
            flash(message, 'success') 
            return redirect(url_for('login'))
        else:
            flash(message, 'error')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        success, user = authenticate_user(email, password)
        if success:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            session['user_pfp'] = user.get('profile_picture', 'base-pfp.png') 
            return redirect(url_for('home'))
        else:
            flash(user, 'error')
    return render_template('login.html')

@app.route('/home')
def home():
    if 'user_id' not in session:
        flash("You must be logged in to view the flood map!", "error")
        return redirect(url_for('login'))

    conn = get_connection()
    user = conn.execute("SELECT username, email, profile_picture FROM users WHERE id = ?", (session['user_id'],)).fetchone()
    if not user:
        flash("User not found!", "error")
        return redirect(url_for('login'))

    session['username'] = user['username']
    session['email'] = user['email']
    session['user_pfp'] = user['profile_picture']

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
                   WHEN events.type = 'traffic_conditions' THEN (SELECT SUBSTR(description, INSTR(description, ':') + 2) FROM traffic_conditions WHERE traffic_conditions.event_id = events.id)
               END AS info
        FROM events
    """
    events = conn.execute(query).fetchall()
    return {"events": [dict(event) for event in events]}

@app.route('/manage_account', methods=['GET', 'POST'])
def manage_account():
    if 'user_id' not in session:
        flash("You must be logged in to manage your account.", "error")
        return redirect(url_for('login'))

    conn = get_connection()
    user_id = session['user_id']
    flash_messages = []

    if request.method == 'POST':
        new_email = request.form.get('email')
        if new_email and new_email != session.get('email'):
            with conn:
                conn.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
            session['email'] = new_email
            flash("Email updated successfully!", "success")

        new_password = request.form.get('password')
        if new_password:
            hashed_password = generate_password_hash(new_password)
            with conn:
                conn.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_password, user_id))
            flash("Password updated successfully!", "success")

        if 'profile_picture' in request.files:
            profile_picture = request.files['profile_picture']
            if profile_picture and profile_picture.filename != '':
                filename = secure_filename(profile_picture.filename)
                file_ext = os.path.splitext(filename)[1].lower()

                if file_ext not in ['.png', '.jpg', '.jpeg']:
                    flash("Invalid file type. Only PNG, JPG, and JPEG are allowed.", "error")
                    return redirect(url_for('manage_account'))

                upload_dir = app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir, exist_ok=True)
                    print(f"Created directory: {upload_dir}")  

                file_path = os.path.join(upload_dir, filename)
                try:
                    profile_picture.save(file_path)
                    print(f"File saved at: {file_path}")  
                except Exception as e:
                    print(f"Error saving file: {e}")  
                    flash("Error uploading the profile picture.", "error")
                    return redirect(url_for('manage_account'))

                conn.execute("UPDATE users SET profile_picture = ? WHERE id = ?", (filename, user_id))
                session['user_pfp'] = filename
                flash("Profile picture updated successfully!", "success")

        for message in flash_messages:
            flash(message, "success")

        return redirect(url_for('manage_account'))

    user = conn.execute("SELECT email, profile_picture FROM users WHERE id = ?", (user_id,)).fetchone()
    return render_template('manage_account.html', user=user)

@app.route('/notification_settings')
def notification_settings():
    if 'user_id' not in session:
        flash("You must be logged in to access notification settings.", "error")
        return redirect(url_for('login'))
    return render_template('notification_settings.html')

@app.route('/statistical_data')
def statistical_data():
    if 'user_id' not in session:
        flash("You must be logged in to view statistical data.", "error")
        return redirect(url_for('login'))
    return render_template('statistical_data.html')

@app.route('/user_history', methods=['GET', 'POST'])
def user_history():
    if 'user_id' not in session:
        flash("You must be logged in to view your history.", "error")
        return redirect(url_for('login'))

    conn = get_connection()
    user_id = session['user_id']
    
    event_type = request.form.get('event_type', 'all')
    date_filter = request.form.get('date', '')

    query = """
        SELECT events.type, events.street, events.city, events.state, events.zip, 
               events.time, events.duration,
               CASE
                   WHEN events.type = 'water_levels' THEN water_levels.level || ' inches'
                   WHEN events.type = 'flood_severity' THEN 'Severity: ' || flood_severity.severity
                   WHEN events.type = 'closed_roads' THEN closed_roads.road_name
                   WHEN events.type = 'flood_reports' THEN 'Risk: ' || flood_reports.risk
                   WHEN events.type = 'traffic_conditions' THEN 'Details: ' || SUBSTR(traffic_conditions.description, INSTR(traffic_conditions.description, ':') + 2)
                   ELSE 'N/A'
               END AS info
        FROM events
        LEFT JOIN water_levels ON events.id = water_levels.event_id
        LEFT JOIN flood_severity ON events.id = flood_severity.event_id
        LEFT JOIN closed_roads ON events.id = closed_roads.event_id
        LEFT JOIN flood_reports ON events.id = flood_reports.event_id
        LEFT JOIN traffic_conditions ON events.id = traffic_conditions.event_id
        WHERE events.user_id = ?
    """

    filters = [user_id]
    if event_type != 'all':
        query += " AND events.type = ?"
        filters.append(event_type)
    if date_filter:
        query += " AND DATE(events.time) = ?"
        filters.append(date_filter)

    query += " ORDER BY events.time DESC"

    reports = conn.execute(query, tuple(filters)).fetchall()

    return render_template('user_history.html', reports=reports)

if __name__ == '__main__':
    app.run(debug=True)
