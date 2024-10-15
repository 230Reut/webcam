
from flask import Flask, flash, redirect, render_template, Response, request, session, url_for, jsonify, send_file
from flask_cors import CORS
import cv2
import io
from datetime import datetime
from data import *

app = Flask(__name__)
CORS(app)

 # Secret key for session management
app.config['SECRET_KEY'] = 'supersecretkey' 
# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        username = request.form['username']

        if password == ACCESS_PASSWORD and username in USERS: 
            
            # Grant access by storing in session
            session['authenticated'] = True
            session['username'] = username
            session['display_name'] = USERS[username]
            return redirect(url_for('index'))
        
        else:
            flash('Invalid password, try again.')
    
    return render_template('login.html')


# Route to log out
@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    session.pop('username', None)
    session.pop('display_name', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))
