import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_connection

def register_user(username, email, password):
    conn = get_connection()
    hashed_password = generate_password_hash(password)
    try:
        with conn:
            conn.execute("""
                INSERT INTO users (username, email, password, profile_picture)
                VALUES (?, ?, ?, ?)
            """, (username, email, hashed_password, 'img/base-pfp.png'))
        return True, "Successfully registered!"
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return False, "Username already taken."
        elif "email" in str(e):
            return False, "Email already registered."
        else:
            return False, "Registration failed."

def authenticate_user(email, password):
    conn = get_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    if user and check_password_hash(user["password"], password):
        return True, {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "profile_picture": user["profile_picture"]
        }
    return False, "Invalid email or password."