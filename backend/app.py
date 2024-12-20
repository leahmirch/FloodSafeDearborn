from flask import Flask, render_template, request, redirect, session, url_for, flash, send_from_directory, jsonify
from .auth import register_user, authenticate_user
from .database import get_connection
from flask_mail import Mail, Message
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objs as go
import plotly
import os
import logging
import json
import base64

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.secret_key = 'secretkey'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'frontend/static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
logging.basicConfig(level=logging.INFO)

mail = Mail(app)

OAUTH2_CREDENTIALS = {
    "installed": {
        "client_id": "1067423235928-g7i50mosc030dmjosgb7ahh5538o9oab.apps.googleusercontent.com",
        "client_secret": "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",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
}

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

TOKEN_FILE = "token.json"

def get_gmail_credentials():
    creds = None
    TOKEN_FILE = "token.json"

    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception as e:
            print("Error loading credentials:", e)
            os.remove(TOKEN_FILE)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(OAUTH2_CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=8080)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds

def send_email_via_gmail(to_email, subject, body):
    creds = get_gmail_credentials()
    service = build('gmail', 'v1', credentials=creds)

    message = f"From: <your-email@gmail.com>\nTo: <{to_email}>\nSubject: {subject}\n\n{body}"
    raw_message = base64.urlsafe_b64encode(message.encode('utf-8')).decode('utf-8')

    try:
        send_message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        print(f"Email sent: {send_message['id']}")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/listings')
def listings():
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page

    event_type = request.args.get('event_type', '')
    date_filter = request.args.get('date', '')

    conn = get_connection()
    query = """
        SELECT * FROM events WHERE 1=1
    """
    filters = []

    if event_type:
        query += " AND type = ?"
        filters.append(event_type)

    if date_filter:
        query += " AND DATE(time) = ?"
        filters.append(date_filter)

    query += " ORDER BY time DESC LIMIT ? OFFSET ?"
    filters.extend([per_page, offset])

    total_query = "SELECT COUNT(*) FROM events WHERE 1=1"
    if event_type:
        total_query += " AND type = ?"
    if date_filter:
        total_query += " AND DATE(time) = ?"

    total_filters = filters[:-2] 
    events = conn.execute(query, filters).fetchall()
    total_events = conn.execute(total_query, total_filters).fetchone()[0]

    next_url = url_for('listings', page=page + 1, event_type=event_type, date=date_filter) if offset + per_page < total_events else None
    prev_url = url_for('listings', page=page - 1, event_type=event_type, date=date_filter) if page > 1 else None

    return render_template('listings.html', events=events, next_url=next_url, prev_url=prev_url)

@app.route('/event/<int:event_id>')
def event_details(event_id):
    conn = get_connection()
    event_query = "SELECT * FROM events WHERE id = ?"
    additional_info_query = """
        SELECT * FROM 
        (
            SELECT 'Water Levels: ' || level AS info FROM water_levels WHERE event_id = ?
            UNION ALL
            SELECT 'Flood Severity: ' || severity FROM flood_severity WHERE event_id = ?
            UNION ALL
            SELECT 'Closed Road: ' || road_name FROM closed_roads WHERE event_id = ?
            UNION ALL
            SELECT 'Flood Risk: ' || risk FROM flood_reports WHERE event_id = ?
            UNION ALL
            SELECT description AS info FROM traffic_conditions WHERE event_id = ?
        )
    """

    event = conn.execute(event_query, (event_id,)).fetchone()
    additional_info = conn.execute(additional_info_query, (event_id, event_id, event_id, event_id, event_id)).fetchall()

    if not event:
        flash("Event not found!", "error")
        return redirect(url_for('listings'))

    return render_template('event_details.html', event=event, additional_info=additional_info)

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
            session['user_pfp'] = user.get('profile_picture', 'img/base-pfp.png') 
            session['admin'] = user.get('admin', 0)
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
    query = request.args.get('query', '').strip().lower()
    search_results = []

    try:
        with open('frontend/static/data/page_content.json', 'r') as file:
            content = json.load(file)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return render_template(
            'search_results.html',
            query=query,
            results=[],
            recommendations=[]
        )

    exclude_pages = ['home', 'interactive_map']  

    pages = []
    corpus = []

    for page, data in content.items():
        if page in exclude_pages:
            continue

        pages.append(page)
        description = data.get("description", "")

        if "sections" in data:
            description += " " + " ".join(data["sections"].values())
        if "tips" in data:
            if isinstance(data["tips"], list):
                description += " " + " ".join(data["tips"])
            elif isinstance(data["tips"], dict):
                for tips_section in data["tips"].values():
                    description += " " + " ".join(tips_section)
        if "contacts" in data:
            description += " " + " ".join(data["contacts"].values())

        corpus.append(description)

    if not query or not corpus or all(desc.strip() == '' for desc in corpus):
        return render_template(
            'search_results.html',
            query=query,
            results=[],
            recommendations=[]
        )

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

    ranked_pages = sorted(zip(pages, similarities), key=lambda x: x[1], reverse=True)

    for page, score in ranked_pages:
        if score > 0:  
            search_results.append({
                'page': page,
                'relevance': "Highly Relevant" if score > 0.6 else "Relevant" if score > 0.3 else "Suggested",
                'display_name': page.replace('_', ' ').title(), 
                'description': content[page]['description']
            })

    recommendations = [
        {
            'page': page,
            'display_name': page.replace('_', ' ').title()
        }
        for page, _ in ranked_pages[:3]
        if page not in exclude_pages
    ]

    return render_template(
        'search_results.html',
        query=query,
        results=search_results,
        recommendations=recommendations
    )

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

            subscribers = conn.execute("""
                SELECT email FROM notifications WHERE notify_email = 1
            """).fetchall()

            email_subject = f"New {event_type.replace('_', ' ').title()} Event Added"
            email_body = f"""
            A new {event_type.replace('_', ' ').title()} event has been reported:
            Location: {street}, {city}, {state}, {zip_code}
            Type: {event_type.replace('_', ' ').title()}
            Duration: {duration} hours

            Please visit Flood Safe Dearborn for more details.
            """

            for subscriber in subscribers:
                try:
                    send_email_via_gmail(subscriber['email'], email_subject, email_body)
                    logging.info(f"Email sent successfully to {subscriber['email']}")
                except Exception as e:
                    logging.error(f"Failed to send email to {subscriber['email']}: {e}")

        flash("Event submitted successfully!", "success")
        return redirect(url_for('home'))

@app.route('/api/events')
def get_events():
    conn = get_connection()
    query = """
        SELECT 
            'flood_history' AS type, 
            latitude, 
            longitude, 
            NULL AS street, 
            NULL AS city, 
            NULL AS state, 
            NULL AS zip, 
            date AS time,
            0 AS duration,
            title AS info
        FROM flood_history

        UNION ALL

        SELECT 
            events.type, 
            events.latitude, 
            events.longitude, 
            events.street, 
            events.city, 
            events.state, 
            events.zip, 
            events.time, 
            events.duration,
            CASE
                WHEN events.type = 'water_levels' THEN 'Water Level: ' || level || ' inches'
                WHEN events.type = 'flood_severity' THEN 'Severity: ' || severity
                WHEN events.type = 'closed_roads' THEN 'Road Closed: ' || road_name
                WHEN events.type = 'flood_reports' THEN 'Flood Risk: ' || risk
                WHEN events.type = 'traffic_conditions' THEN description
                ELSE 'N/A'
            END AS info
        FROM events
        LEFT JOIN water_levels ON events.id = water_levels.event_id
        LEFT JOIN flood_severity ON events.id = flood_severity.event_id
        LEFT JOIN closed_roads ON events.id = closed_roads.event_id
        LEFT JOIN flood_reports ON events.id = flood_reports.event_id
        LEFT JOIN traffic_conditions ON events.id = traffic_conditions.event_id
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
        new_password = request.form.get('password')
        profile_picture = request.files.get('profile_picture')

        if new_email and new_email != session.get('email'):
            with conn:
                conn.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
            session['email'] = new_email
            flash("Email updated successfully!", "success")

        if new_password:
            hashed_password = generate_password_hash(new_password)
            with conn:
                conn.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_password, user_id))
            flash("Password updated successfully!", "success")

        if profile_picture and profile_picture.filename:
            filename = secure_filename(profile_picture.filename)
            file_ext = os.path.splitext(filename)[1].lower()

            if file_ext not in ['.png', '.jpg', '.jpeg']:
                flash("Invalid file type. Only PNG, JPG, and JPEG are allowed.", "error")
            else:
                upload_dir = app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir, exist_ok=True)

                file_path = os.path.join(upload_dir, filename)
                profile_picture.save(file_path)

                conn.execute("UPDATE users SET profile_picture = ? WHERE id = ?", (f'uploads/{filename}', user_id))
                session['user_pfp'] = f'uploads/{filename}'
                flash("Profile picture updated successfully!", "success")

        return redirect(url_for('manage_account'))

    user = conn.execute("SELECT email, profile_picture FROM users WHERE id = ?", (user_id,)).fetchone()
    return render_template('manage_account.html', user=user)

@app.route('/notification_settings', methods=['GET', 'POST'])
def notification_settings():
    if 'user_id' not in session:
        flash("You must be logged in to manage notifications.", "error")
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    conn = get_connection()
    user = conn.execute("SELECT email FROM users WHERE id = ?", (user_id,)).fetchone()

    if request.method == 'POST':
        email = request.form['email']
        notify_email = 1 if request.form.get('notify_email') else 0
        
        conn.execute("""
            INSERT OR REPLACE INTO notifications (user_id, email, notify_email)
            VALUES (?, ?, ?)
        """, (user_id, email, notify_email))

        conn.execute("""
            UPDATE users SET subscriber = ? WHERE id = ?
        """, (notify_email, user_id))

        conn.commit()

        if notify_email:
            send_email_via_gmail(email, "Thank you for subscribing!", 
                                 "Thank you for subscribing to flood notifications from Flood Safe Dearborn!")
        
        flash("Notification settings updated!", "success")
        return redirect(url_for('notification_settings'))
    
    settings = conn.execute("SELECT email, notify_email FROM notifications WHERE user_id = ?", (user_id,)).fetchone()
    return render_template(
        'notification_settings.html',
        user_email=settings['email'] if settings else user['email'],
        notify_email=settings['notify_email'] if settings else 0
    )

def send_subscription_email(user_email):
    msg = Message("Thank you for subscribing to flood notifications!",
                  recipients=[user_email])
    msg.body = "Thank you for subscribing to flood notifications from Flood Safe Dearborn! Stay safe and stay informed."
    with app.app_context():
        mail.send(msg)

@app.route('/statistical_data')
def statistical_data():
    conn = get_connection()
    
    events_by_type = conn.execute("""
        SELECT type, COUNT(*) AS count
        FROM events
        GROUP BY type
    """).fetchall()
    
    severity_distribution = conn.execute("""
        SELECT severity, COUNT(*) AS count
        FROM flood_severity
        GROUP BY severity
    """).fetchall()

    events_per_year = conn.execute("""
        SELECT strftime('%Y', time) AS year, COUNT(*) AS count
        FROM events
        GROUP BY year
        ORDER BY year
    """).fetchall()

    events_by_type_data = [{"type": row["type"], "count": row["count"]} for row in events_by_type]
    severity_data = [{"severity": row["severity"], "count": row["count"]} for row in severity_distribution]
    events_per_year_data = [{"year": row["year"], "count": row["count"]} for row in events_per_year]

    return render_template(
        'statistical_data.html',
        events_by_type=events_by_type_data,
        severity_data=severity_data,
        events_per_year=events_per_year_data
    )

@app.route('/interactive-chart')
def interactive_chart():
    import plotly.graph_objs as go
    from plotly.utils import PlotlyJSONEncoder

    years = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
    damage = [50, 75, 60, 80, 95, 70, 110, 150]

    fig = go.Figure(data=[
        go.Bar(x=years, y=damage, marker_color='blue', name="Flood Damage")
    ])
    fig.update_layout(
        title="Flood Damage in Dearborn, MI (2014-2021)",
        xaxis_title="Year",
        yaxis_title="Damage (in millions of USD)",
        template="plotly_white"
    )

    chart_json = json.dumps(fig, cls=PlotlyJSONEncoder)
    return render_template('interactive_chart.html', chart_json=chart_json)

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

@app.route('/admin/manage_users', methods=['GET', 'POST'])
def admin_manage_users():
    if not session.get('admin') == 1:
        flash("Access denied: Admins only!", "error")
        return redirect(url_for('home'))

    conn = get_connection()

    if request.method == 'POST':
        user_id = request.form['user_id']

        if 'update' in request.form:
            new_username = request.form.get('new_username')
            new_password = request.form.get('new_password')
            if new_username:
                conn.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
            if new_password:
                hashed_password = generate_password_hash(new_password)
                conn.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_password, user_id))
            flash("User updated successfully!", "success")

        elif 'promote' in request.form:
            conn.execute("UPDATE users SET admin = 1 WHERE id = ?", (user_id,))
            flash("User promoted to admin successfully!", "success")

        elif 'delete' in request.form:
            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            flash("User deleted successfully!", "success")

        conn.commit()
        return redirect(url_for('admin_manage_users'))

    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page

    users = conn.execute("SELECT id, username, email, password, profile_picture, admin FROM users LIMIT ? OFFSET ?", 
                         (per_page, offset)).fetchall()
    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]

    next_url = url_for('admin_manage_users', page=page + 1) if offset + per_page < total_users else None
    prev_url = url_for('admin_manage_users', page=page - 1) if page > 1 else None

    return render_template('admin_manage_users.html', users=users, next_url=next_url, prev_url=prev_url)

@app.route('/admin/manage_events', methods=['GET', 'POST'])
def admin_manage_events():
    if not session.get('admin') == 1:
        flash("Access denied: Admins only!", "error")
        return redirect(url_for('home'))

    conn = get_connection()

    if request.method == 'POST':
        event_id = request.form.get('event_id')

        if 'update_address' in request.form:
            new_street = request.form.get('street')
            new_city = request.form.get('city')
            new_state = request.form.get('state')
            new_zip = request.form.get('zip')

            conn.execute("""
                UPDATE events
                SET street = ?, city = ?, state = ?, zip = ?
                WHERE id = ?
            """, (new_street, new_city, new_state, new_zip, event_id))
            flash("Address updated successfully!", "success")

        elif 'update_duration' in request.form:
            new_duration = request.form.get('duration')
            conn.execute("""
                UPDATE events
                SET duration = ?
                WHERE id = ?
            """, (new_duration, event_id))
            flash("Duration updated successfully!", "success")

        elif 'update_time' in request.form:
            new_time = request.form.get('time')
            conn.execute("""
                UPDATE events
                SET time = ?
                WHERE id = ?
            """, (new_time, event_id))
            flash("Date/Time updated successfully!", "success")

        elif 'update_details' in request.form:
            event_type = conn.execute("SELECT type FROM events WHERE id = ?", (event_id,)).fetchone()[0]
            new_details = request.form.get('details')

            if event_type == 'water_levels':
                conn.execute("UPDATE water_levels SET level = ? WHERE event_id = ?", (new_details, event_id))
            elif event_type == 'flood_severity':
                conn.execute("UPDATE flood_severity SET severity = ? WHERE event_id = ?", (new_details, event_id))
            elif event_type == 'closed_roads':
                conn.execute("UPDATE closed_roads SET road_name = ? WHERE event_id = ?", (new_details, event_id))
            elif event_type == 'flood_reports':
                conn.execute("UPDATE flood_reports SET risk = ? WHERE event_id = ?", (new_details, event_id))
            elif event_type == 'traffic_conditions':
                conn.execute("UPDATE traffic_conditions SET description = ? WHERE event_id = ?", (new_details, event_id))

            flash("Details updated successfully!", "success")

        elif 'delete' in request.form:
            conn.execute("DELETE FROM events WHERE id = ?", (event_id,))
            flash("Event deleted successfully!", "success")

        conn.commit()
        return redirect(url_for('admin_manage_events'))

    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page

    events = conn.execute("""
        SELECT events.id, events.type, events.street, events.city, events.state, events.zip,
               events.time, events.duration, users.username AS submitted_by,
               CASE 
                   WHEN events.type = 'water_levels' THEN water_levels.level || ' inches'
                   WHEN events.type = 'flood_severity' THEN 'Severity: ' || flood_severity.severity
                   WHEN events.type = 'closed_roads' THEN closed_roads.road_name
                   WHEN events.type = 'flood_reports' THEN 'Risk: ' || flood_reports.risk
                   WHEN events.type = 'traffic_conditions' THEN traffic_conditions.description
                   ELSE 'N/A'
               END AS details
        FROM events
        LEFT JOIN users ON events.user_id = users.id
        LEFT JOIN water_levels ON events.id = water_levels.event_id
        LEFT JOIN flood_severity ON events.id = flood_severity.event_id
        LEFT JOIN closed_roads ON events.id = closed_roads.event_id
        LEFT JOIN flood_reports ON events.id = flood_reports.event_id
        LEFT JOIN traffic_conditions ON events.id = traffic_conditions.event_id
        LIMIT ? OFFSET ?
    """, (per_page, offset)).fetchall()

    parsed_events = []
    for event in events:
        event = dict(event)
        if event['time']:
            try:
                event['time'] = datetime.strptime(event['time'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                event['time'] = None
        parsed_events.append(event)

    total_events = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]

    next_url = url_for('admin_manage_events', page=page + 1) if offset + per_page < total_events else None
    prev_url = url_for('admin_manage_events', page=page - 1) if page > 1 else None

    return render_template('admin_manage_events.html', events=parsed_events, next_url=next_url, prev_url=prev_url)

if __name__ == '__main__':
    app.run(debug=True)
