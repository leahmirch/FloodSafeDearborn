import sqlite3
from werkzeug.security import generate_password_hash

DB_FILE = 'floodsafe_db.sqlite'

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    conn = get_connection()
    with conn:

        # Users table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                profile_picture TEXT DEFAULT 'img/base-pfp.png',
                admin INTEGER DEFAULT 0 CHECK(admin IN (0, 1)),
                subscriber INTEGER DEFAULT 0 CHECK(subscriber IN (0, 1))
            )
        """)
        
        # Events table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                street TEXT,
                city TEXT,
                state TEXT,
                zip TEXT,
                latitude REAL,
                longitude REAL,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                duration INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Index for efficient pagination on events
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_time ON events (time DESC)
        """)
        
        # Notifications table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                email TEXT,
                notify_email INTEGER DEFAULT 0 CHECK(notify_email IN (0, 1)),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # Water levels table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS water_levels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER NOT NULL,
                level INTEGER NOT NULL,
                FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
            )
        """)
        
        # Flood severity table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS flood_severity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER NOT NULL,
                severity TEXT CHECK(severity IN ('Low', 'Moderate', 'High')),
                FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
            )
        """)
        
        # Closed roads table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS closed_roads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER NOT NULL,
                road_name TEXT NOT NULL,
                FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
            )
        """)
        
        # Flood reports table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS flood_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER NOT NULL,
                risk TEXT CHECK(risk IN ('Low', 'Moderate', 'High')),
                FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
            )
        """)
        
        # Traffic conditions table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS traffic_conditions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
            )
        """)

        # Add a general metadata table for future scalability
        conn.execute("""
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)

        # Flood history table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS flood_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                date TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                location TEXT NOT NULL
            )
        """)

        # Insert default admin user
        admin_username = "admin"
        admin_email = "floodsafedearborn@gmail.com"
        admin_password = generate_password_hash("admin123")
        admin_check = conn.execute("SELECT * FROM users WHERE username = ?", (admin_username,)).fetchone()

        if not admin_check:
            conn.execute("""
                INSERT INTO users (username, email, password, profile_picture, admin)
                VALUES (?, ?, ?, ?, ?)
            """, (admin_username, admin_email, admin_password, 'img/base-pfp.png', 1))
            print("Admin user successfully created.")

        # Insert flood history events
        print("Inserting flood history events...")
        flood_events = [
            ("The Rouge River Flood - Most Severe Flood Event", "April 1947", 42.3223, -83.1766, "Rouge River,"),
            ("Flood Event", "August 2007", 42.3163, -83.2736, "Michigan Avenue"),
            ("Flood Event", "June 2008", 42.3202, -83.1874, "Outer Drive"),
            ("Flood Event", "August 2009", 42.3314, -83.2116, "Evergreen Road"),
            ("Flood Event", "June 2010", 42.3093, -83.2344, "Ford Road"),
            ("Severe Flood Event", "July 2013", 42.3221, -83.1945, "Greenfield Road"),
            ("Severe Flood Event", "August 2014", 42.3230, -83.2250, "Rotunda Drive"),
            ("Most Recent Flooding - Severe Flood Event", "July 2021", 42.3191, -83.1978, "Michigan Avenue & Greenfield, Dearborn, MI"),
        ]

        for title, date, latitude, longitude, location in flood_events:
            conn.execute("""
                INSERT OR IGNORE INTO flood_history (title, date, latitude, longitude, location)
                VALUES (?, ?, ?, ?, ?)
            """, (title, date, latitude, longitude, location))

        print("Predefined flood history events inserted successfully.")

setup_database()
