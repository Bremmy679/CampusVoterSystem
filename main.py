from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, flash, jsonify
import os
import re
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

import base64
from flask_mail import Mail, Message
import binascii



app = Flask(__name__)
SECRET_KEY = Fernet.generate_key()
app.config['SECRET_KEY'] = 'secret'
cipher_suite = Fernet(SECRET_KEY)
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = '*******'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


def get_db_connection():
    conn = sqlite3.connect('electiondb.db')
    conn.row_factory = sqlite3.Row
    return conn

    
def sendMail():
    msg = Message('Hello', sender = 'ogolasospeter62@gmail.com', recipients = ['captainsos483@gmail.com'])
    msg.body = "Hello Flask message sent from Flask-Mail"
    mail.send(msg)
    return "Sent"

# The user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    campuses = getCampuses()
    colleges = getColleges()
    error = None
    msg = None

    if request.method == 'POST':
        useremail = request.form['useremail']
        password = request.form['password']
        userRegNo = request.form['userRegNo']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        college = request.form['college']
        school = request.form['school']
        course = request.form['course']
        userIdNo = request.form['userIdNo']
        campus = request.form['campus']
        academicyear = request.form['academicyear']
        userName = firstName + " " + lastName

        if not is_valid_email(useremail):
            error = 'Invalid email format.'
        if not is_valid_password(password):
            error = 'Password must be at least 8 characters long.'
        
        user = get_user(useremail)
        if user is not None:
            error = 'User already exists.'
        else:
<<<<<<< HEAD
            return render_template('register.html', error='Invalid occurrences in field(s).')
    return render_template('registration_page.html')
=======
            registeruser(useremail, password, userName, userRegNo, college, course, school, campus, academicyear,
                             userIdNo)
            msg = "Record successfully added"
            return redirect(url_for('home'))

    return render_template('register.html',msg = msg,error=error, campuses=campuses, colleges=colleges)



>>>>>>> 16b626cc26395232d0045890202486c588d1cab2

#Register user function
def registeruser(email, password,name,regNo,college,course,school,campus,academicyear,userIdNo):
    conn = get_db_connection()
    conn.execute('INSERT INTO voters (email, password,name,regNo,college,course,school,campus,academicyear,idNo) VALUES (?,?,?,?,?,?,?,?,?,?)', (encrypt_data(email), hash_password(password),encrypt_data(name),encrypt_data(regNo),encrypt_data(college),course),school),encrypt_data(campus),encrypt_data(academicyear),encrypt_data(userIdNo)
    conn.commit()
    conn.close()
    return True

#The login Page handler
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        useremail = request.form['useremail']
        password = request.form['password']
        user = get_user(useremail)

        # Check if user exists
        if user is None:
            return render_template('login.html', error='User does not exist.')
        # Check if useremail and password are provided
        if not useremail or not password:
            return render_template('login.html', error='Please provide both email and password.')


        # Check email format
        if not is_valid_email(useremail):
            return render_template('login.html', error='Invalid email format.')

        # Check password length
        if not is_valid_password(password):
            return render_template('login.html', error='Password must be at least 8 characters long.')

        

        # Check password
        if not check_password(password, user['password']):
            return render_template('login.html', error='Incorrect email or password.')

        # Set user email in session
        session['useremail'] = useremail

        return redirect(url_for('home'))

    return render_template('login.html')

<<<<<<< HEAD
#dashboard page
@app.route("/")
def dashboard():
    return render_template('dashboard.html')

@app.route("/admin")
def create_admin():
    return render_template('create_admin_account.html')

#get user from the database
=======
>>>>>>> 16b626cc26395232d0045890202486c588d1cab2
def get_user(useremail):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM voters WHERE email = ?', (encrypt_data(useremail),)).fetchone()
    conn.close()
    return dict(user) if user else None


#The password hashing function
def hash_password(password):
    return generate_password_hash(password)


def check_password(password, hashed_password):
    return check_password_hash(hashed_password, password)



#logout
@app.route('/logout')
def logout():
    if 'useremail' in session:
        session['useremail'] = None
        flash(f"{session['useremail']}  successfully logged Out.")

    return redirect(url_for('home'))


#The IndexPage
@app.route('/index/<electiondata>')
def index(electiondata):
    if electiondata.isNotEmpty():
        return render_template('index.html', electiondata=electiondata)

    else:
        return render_template('index.html', electiondata="No Data Found")

#The landing Page Handler
@app.route('/home')
def home():
    cursor = get_db_connection().cursor()
    cursor.execute('SELECT DISTINCT name, id,email,campus,school,regNo,password FROM candidates')
    rows = cursor.fetchall()

     # Fetch campuses, colleges, schools, and courses data
    cursor.execute('SELECT DISTINCT name FROM campuses')
    campuses = [row['name'] for row in cursor.fetchall()]

    cursor.execute('select DISTINCT college FROM courseGrouped')
    colleges = [row['college'] for row in cursor.fetchall()]

    cursor.execute('select DISTINCT school FROM courseGrouped')
    schools = [row['school'] for row in cursor.fetchall()]

    cursor.execute('select DISTINCT course FROM courseGrouped')
    courses = [row['course'] for row in cursor.fetchall()]

  
   
    return render_template('votesResult.html', rows=rows,colleges=colleges,campuses=campuses,schools=schools,courses=courses)

#Email Validation
def is_valid_email(email):
    return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)
    

#Password Validation
def is_valid_password(password):
    if len(password) < 8:
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
            reg_no = request.form['regNo']
            position = request.form['position']

            

            connection = self.get_db_connection()
            cursor = connection.cursor()
            user = getcandidatefromvoters(reg_no)
            positionId = getpostid(position)
            connection.commit()
            msg = "Record successfully fetched."

            created= time().time()
            name = user.name
            regNo = user.regNo
            email=  user.email
            password= user.password
            college = user.college
            school= user.school
            course= user.course
            campus= user.campus
            academicYear= user.academicYear
            userIdNo= user.userIdNo

            conn = self.get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO candidates (name, reg_no, college, acad_year, electedPost_id,idNo) VALUES (?, ?, ?, ?, ?,?)", (encrypt_data(name), encrypt_data(reg_no), encrypt_data(college), encrypt_data(acad_year), encrypt_data(positionId),encrypt_data(userIdNo)))
            conn.commit()
            msg = "Record successfully added"
            if session.addcandidate(name, reg_no, college, acad_year, position):
                return redirect(url_for('home'))
            else:
                return render_template('addcandidate.html', error='Invalid occurrences in field(s)')
        except:
            conn.rollback()
            msg = "error in insert operation"
      
        finally:
            return render_template("success.html",msg = msg)
            con.close()

    return render_template('addcandidate.html')


#Get the candidate data based on regNo
def getcandidatefromvoters(regno):
    conn = get_db_connection()
    candidate = conn.execute('SELECT * FROM voters WHERE regNo = ?', (regno,)).fetchone()
    conn.close()
    return candidate

def getpostid(name):
    conn = get_db_connection()
    postid = conn.execute('SELECT id FROM posts WHERE name = ?', (encrypt_data(name),)).fetchone()

def getCampuses():
    conn = get_db_connection()
    encrypted_campuses = conn.execute('SELECT name FROM campuses').fetchall()
    conn.close()
    decrypted_campuses = [decrypt_data(campus['name']) for campus in encrypted_campuses]
    
    print("Encrypted Campuses:", encrypted_campuses)
    print("Decrypted Campuses:", decrypted_campuses)
    
    return decrypted_campuses


def getColleges():
    conn = get_db_connection()
    encrypted_colleges = conn.execute('SELECT DISTINCT college FROM courseGrouped').fetchall()
    conn.close()
    decrypted_colleges = [decrypt_data(college['college']) for college in encrypted_colleges]
    return decrypted_colleges

def getSchools(college):
    conn = get_db_connection()
    encrypted_schools = conn.execute('SELECT DISTINCT  school FROM courseGrouped WHERE college = ?',(encrypt_data(college),)).fetchall()
    conn.close()
    decrypted_schools = [decrypt_data(school['school']) for school in encrypted_schools]
    return decrypted_schools

def getCourses(school):
    conn = get_db_connection()
    courses = conn.execute('SELECT DISTINCT course FROM courseGrouped WHERE school = ?',(encrypt_data(school),)).fetchall()
    conn.close()
    decrypted_courses = [decrypt_data(course['course']) for course in courses]
    return decrypted_courses

# In your /get_schools route
@app.route('/get_schools', methods=['GET'])
def get_schools():
    selected_college = request.args.get('college')
    schools = getSchools(selected_college)
    return jsonify(schools=[{'school': school['school']} for school in schools])


@app.route('/get_courses', methods=['GET'])
def get_courses():
    selected_school = request.args.get('school')
    courses = getCourses(selected_school)
    return jsonify(courses=[{'course':course['course']}for course in courses])


#Edit a candidate data
@app.route('/editcandidate/<reg_no>', methods=['GET', 'POST'])
def editcandidate(regno):
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
            cur.execute("UPDATE candidates SET name=?, college=?, academicyear=?, position=? WHERE regNo=?", (encrypt_data(name), encrypt_data(college), encrypt_data(acad_year), encrypt_data(position), encrypt_data(regno)))
            conn.commit()
            msg = "Record successfully updated"
            if session.editcandidate(encrypt_data(name), encrypt_data(regno), encrypt_data(college), encrypt_data(acad_year), encrypt_data(position)):
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
            cur.execute("SELECT * FROM candidates WHERE reg_no=?", (encrypt_data(reg_no)))
            conn.commit()
            msg = "Record successfully updated"
            if session.editcandidate(encrypt_data(name), encrypt_data(reg_no), encrypt_data(college),encrypt_data(acad_year),encrypt_data(position)):
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
@app.route('/deletecandidate/<regno>', methods=['GET', 'POST'])
def deletecandidate(regno):

    if request.method == 'POST':
        try:
            session = Session()
            reg_no = request.form['regNo']

            self.get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM candidates WHERE regNo=?", (encrypt_data(regno)))
            conn.commit()
            msg = f"Candidate {decrypt_data(reg_no)} successfully deleted"
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

#The electionvotes
def electionvotes():
    cursor = get_db_connection().cursor()
    cursor.execute('SELECT * FROM candidates')
    rows = cursor.fetchall()
   
    return  rows

#The results Page
@app.route('/results')
def results():
    electedcandidates = electionvotes()
    if len(electedcandidates) > 1:
        return render_template('results.html', electedcandidates=electedcandidates)

    else:
        return render_template('results.html', electedcandidates="No Data Found")
     


@app.route('/vote_counts')
def vote_counts():
    cursor = get_db().cursor()
    cursor.execute('SELECT name, votes FROM candidates')
    rows = cursor.fetchall()
    return jsonify(rows)

#Data Security functions
def encrypt_data(data):
    encrypted_data = cipher_suite.encrypt(data.encode())
    return base64.urlsafe_b64encode(encrypted_data).decode()

def decrypt_data(encrypted_data):
    try:
        decoded_data = base64.urlsafe_b64decode(encrypted_data)
        decrypted_data = cipher_suite.decrypt(decoded_data).decode()
        return decrypted_data
    except binascii.Error as e:
        print(f"Error decoding base64: {e}")
    except InvalidToken:
        print("Invalid Fernet token. Data may have been tampered with.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None




if __name__ == '__main__':
    app.run(debug=True) #debug=True is optional