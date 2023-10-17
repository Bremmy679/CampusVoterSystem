from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from session import Session
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


#The login Page handler
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session = Session()
        useremail = request.form['useremail']
        password = request.form['password']
        if not is_valid_email(useremail):
            return render_template('login.html', error='Invalid email format.')
        if not is_valid_password(password):
            return render_template('login.html', error='Password must be at least 8 characters long.')
        if session.login(username, password):
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid useremail or password')
    return render_template('login.html')


#The landing Page Handler
@app.route('/')
def home():
    return render_template('home.html')


#Email Validation
def is_valid_email(email):
    re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)

#Password Validation
def is_valid_password(password):
    if password.length < 8:
        return False
    return True

if __name__ == '__main__':
    app.run(debug=True)