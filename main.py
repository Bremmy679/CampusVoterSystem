from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from session import Session
import re
import sqlite3
from wekzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


def get_db_connection():
    conn = sqlite3.connect('electiondb.db')
    conn.row_factory = sqlite3.Row
    return conn

#The user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        session = Session()
        useremail = request.form['useremail']
        password = request.form['password']
        session['useremail'] = useremail
        if not is_valid_email(useremail):
            return render_template('register.html', error='Invalid email format.')
        if not is_valid_password(password):
            return render_template('register.html', error='Password must be at least 8 characters long.')

        user = get_user(useremail)
        if user is not None:
            return render_template('register.html', error='User already exists.')
        if session.registeruser(useremail, password):
            return redirect(url_for('home'))
        else:
            return render_template('register.html', error='Invalid occurrences in field(s).')
    return render_template('register.html')

#The login Page handler
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session = Session()
        useremail = request.form['useremail']
        password = request.form['password']
        session['useremail'] = useremail
        if not is_valid_email(useremail):
            return render_template('login.html', error='Invalid email format.')
        if not is_valid_password(password):
            return render_template('login.html', error='Password must be at least 8 characters long.')

        user = get_user(useremail)
        if user is None:
            return render_template('login.html', error='User does not exist.')
        if not check_password(password, user.password):
            return render_template('login.html', error='Incorrect email or password.')
        return redirect(url_for('home'))
      
    return render_template('login.html')

#logout
@app.route('/logout')
def logout():
    if 'useremail' in session:
        session['useremail'] = None
        flash(f"{session['useremail']}  successfully logged Out.")

    return redirect(url_for('home'))


#The IndexPage
@app.route('/index','<electiondata>')
def index(electiondata):
    if electiondata.isNotEmpty():
        return render_template('index.html', electiondata=electiondata)

    else:
        return render_template('index.html', electiondata="No Data Found")

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

#Add Candidate Page
@app.route('/newcandidate')
def newcandidate():
    return render_template('newcandidate.html')

@app.route('/addcandidate', methods=['GET', 'POST'])
def addcandidate():
    if request.method == 'POST':
        try:
            session = Session()
            name = request.form['name']
            reg_no = request.form['regNo']
            college = request.form['college']
            acad_year = request.form['acadYear']
            position = request.form['position']

            self.get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO candidates (name, reg_no, college, acad_year, position) VALUES (?, ?, ?, ?, ?)", (name, reg_no, college, acad_year, position))
            conn.commit()
            msg = "Record successfully added"
            if session.addcandidate(name, reg_no, college, acad_year, position):
                return redirect(url_for('home'))
            else:
                return render_template('addcandidate.html', error='Invalid occurrences in field(s))')
        except:
            conn.rollback()
            msg = "error in insert operation"
      
        finally:
            return render_template("success.html",msg = msg)
            con.close()

    return render_template('addcandidate.html')

#Edit a candidate data
@app.route('/editcandidate/<reg_no:String>', methods=['GET', 'POST'])
def editcandidate(reg_no):
    if request.method == 'POST':
        try:
            session = Session()
            name = request.form['name']
            reg_no = request.form['regNo']
            college = request.form['college']
            acad_year = request.form['acadYear']
            position = request.form['position']

            self.get_db_connection()
            cur = conn.cursor()
            cur.execute("UPDATE candidates SET name=?, college=?, acad_year=?, position=? WHERE reg_no=?", (name, college, acad_year, position, reg_no))
            conn.commit()
            msg = "Record successfully updated"
            if session.editcandidate(name, reg_no, college, acad_year, position):
                return redirect(url_for('home'))
            else:
                return render_template('editcandidate.html', error='Invalid occurrences in field(s))')
        except:
            conn.rollback()
            msg = "error in update operation"
      
        finally:
            return render_template("success.html",msg = msg)
            con.close()

    if request.method == 'GET':
        try:
            session = Session()
            name = request.form['name']
            reg_no = request.form['regNo']
            college = request.form['college']
            acad_year = request.form['acadYear']
            position = request.form['position']

            self.get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM candidates WHERE reg_no=?", (reg_no))
            conn.commit()
            msg = "Record successfully updated"
            if session.editcandidate(name, reg_no, college, acad_year, position):
                return redirect(url_for('home'))
            else:
                return render_template('editcandidate.html', error='Invalid occurrences in field(s))')
        except:
            conn.rollback()
            msg = "error in update operation"
      
        finally:
            return render_template("success.html",msg = msg)
            con.close()

    return render_template('editcandidate.html')



#Delete a candidate data
@app.route('/deletecandidate/<reg_no:String>', methods=['GET', 'POST'])
def deletecandidate(reg_no):

    if request.method == 'POST':
        try:
            session = Session()
            reg_no = request.form['regNo']

            self.get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM candidates WHERE reg_no=?", (reg_no))
            conn.commit()
            msg = f"Candidate {reg_no} successfully deleted"
            if session.deletecandidate(reg_no):
                return redirect(url_for('home'))
            else:
                return render_template('deletecandidate.html', error='The candidate could not be deleted.')
        except:
            conn.rollback()
            msg = "Error in delete operation"
    
        finally:
            return render_template("success.html",msg = msg)
            con.close()


    return render_template('deletecandidate.html')

#Register user function
def registeruser(email,password):
    conn = get_db_connection
    conn.execute('INSERT INTO user (useremail, password) VALUES (?, ?)', (email, hash_password(password)))
    conn.commit()
    conn.close()
    return True
     

#get user from the database
def get_user(useremail):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE useremail = ?', (useremail,)).fetchone()
    conn.close()
    return user

#The password hashing function
def hash_password(password):
    return generate_password_hash(password)

def check_password(password, user):
    
    return check_password_hash(user.password, password)

if __name__ == '__main__':
    app.run(debug=True) #debug=True is optional