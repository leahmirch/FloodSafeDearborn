from flask import Flask, render_template, request, redirect, session, url_for, flash
from auth import register_user, authenticate_user
from database import get_connection
import os

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
        return redirect(url_for('login'))

    conn = get_connection()
    user = conn.execute("SELECT username FROM users WHERE id = ?", (session['user_id'],)).fetchone()
    if not user:
        flash("User not found!")
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

if __name__ == '__main__':
    app.run(debug=True)
