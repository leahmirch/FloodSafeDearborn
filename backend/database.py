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
                admin INTEGER DEFAULT 0 CHECK(admin IN (0, 1))
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

        # Insert default admin user
        admin_username = "admin"
        admin_email = "admin@floodsafe.com"
        admin_password = generate_password_hash("admin123")
        admin_check = conn.execute("SELECT * FROM users WHERE username = ?", (admin_username,)).fetchone()

        if not admin_check:
            conn.execute("""
                INSERT INTO users (username, email, password, profile_picture, admin)
                VALUES (?, ?, ?, ?, ?)
            """, (admin_username, admin_email, admin_password, 'img/base-pfp.png', 1))
            print("Admin user successfully created.")

setup_database()
