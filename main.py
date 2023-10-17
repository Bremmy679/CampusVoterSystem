from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


#The login Page handler
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session = Session()
        username = request.form['username']
        password = request.form['password']
        if session.login(username, password):
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')


#The landing Page Handler
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)