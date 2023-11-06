from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, flash, jsonify, current_app
import os
import re
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import logging


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
@app.route('/Register Student', methods=['GET', 'POST'])
def register():
    campuses = getCampuses()
    colleges = getColleges()
    error = None
    msg = None

    if request.method == 'POST':
        useremail = request.form['useremail']
        password = request.form['password']
        userRegNo = request.form['registrationNo']
        college = request.form['college']
        school = request.form['school']
        course = request.form['course']
        userIdNo = request.form['idNo']
        campus = request.form['campus']
        academicyear = request.form['academicyear']
        userName = request.form['username']
        if not is_valid_email(useremail):
            error = 'Invalid email format.'
        if not is_valid_password(password):
            error = 'Password must be at least 8 characters long.'
        
        user = get_user(useremail)
        passwords = get_passwords()
        idNos = get_idNos()
        
        if user is not None:
            error = 'User already exists.'
            flash(error,category = "error")
        else:
            for passwd in passwords:
                if check_password_hash(password,passwd):
                    error = 'Password already exists. Try a different Password.'
                    flash(error,category="error")
                else:
                    continue
            if userIdNo in idNos:
                error = 'The ID already exists!!!'
                flash(error,category="error")
            else:
                registeruser(useremail, password, userName, userRegNo, college, course, school, campus, academicyear,
                                userIdNo)
                msg = "Record successfully added"
                flash(message=msg, category="success")
                return redirect(url_for('login'))

    return render_template('registration_page.html',msg = msg,error=error, campuses=campuses, colleges=colleges)

#Register user function
def registeruser(email, password,name,regNo,college,course,school,campus,academicyear,userIdNo):
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO voters (email, password, name, regNo, college, course, school, campus, academicyear, idNo) VALUES (?,?,?,?,?,?,?,?,?,?)', (email, hash_password(password), name, regNo, college, course, school, campus, academicyear, userIdNo))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Handle the case where the idNo already exists
        error = f"User with ID {userIdNo} already exists."
        return False
    finally:
        conn.close()
    # conn.execute('INSERT INTO voters (email, password,name,regNo,college,course,school,campus,academicyear,idNo) VALUES (?,?,?,?,?,?,?,?,?,?)', (email, password,name,regNo,college,course,school,campus,academicyear,userIdNo))
    # conn.commit()
    # conn.close()
    # return True

#The login Page handler
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    msg = None
    if request.method == 'POST':
        useremail = request.form['useremail']
        password = request.form['password']

        # Check if both email and password are provided
        if not useremail or not password:
            return render_template('login.html', error='Please provide both email and password.')
            error = 'Please provide both email and password.'
            flash(error, category="error")

        # Check email format
        if not is_valid_email(useremail):
            return render_template('login.html', error='Invalid email format.')
            error = 'Invalid email format.'
            flash(error, category="error")

        # Check password length
        if not is_valid_password(password):
            return render_template('login.html', error='Password must be at least 8 characters long.')
            error = 'Password must be at least 8 characters long.'
            flash(error, category="error")

        user = get_user(useremail)

        # Check if user exists
        if user is None:
            return render_template('login.html', error='User does not exist.')
            error = 'User does not exist.'
            flash(error, category="error")

        # Check password
        if not check_password(password, user['password']):
            return render_template('login.html', error='Incorrect email or password.')
            error = 'Incorrect email or password.'
            flash(error, category="error")

        # Set user email in session
        session['useremail'] = useremail

        return redirect(url_for('dashboard'))
        msg = f"{session['useremail']} successfully logged in."
        flash(msg,category="success")

    return render_template('login.html',error=error,msg=msg)

#dashboard page
@app.route("/dashboard")
def dashboard():
    positions = get_posts()
    Positions = [position['name'].upper() for position in positions]
    return render_template('dashboard.html',Positions=Positions,positions=positions)

@app.route("/Register Admin")
def create_admin():
    return render_template('create_admin_account.html')

#get user from the database
def get_user(useremail):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM voters WHERE email = ?', (useremail,)).fetchone()
    conn.close()
    return dict(user) if user else None
def get_passwords():
    conn = get_db_connection()
    encrypted_passwords = conn.execute('SELECT password FROM voters').fetchall()
    
    conn.close()
    return encrypted_passwords

def get_idNos():
    conn = get_db_connection()
    idNos = conn.execute('SELECT idNo FROM voters').fetchall()
    conn.close()
    id = [idNo['idNo'] for idNo in idNos]
    return id


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
@app.route('/HomePage')
def home():
    cursor = get_db_connection().cursor()
    cursor.execute('SELECT DISTINCT name, id,email,campus,school,regNo FROM candidates')
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
    posts = get_posts()
    msg = None
    error = None
    if request.method == 'POST':
        conn = get_db_connection()
        try:
            
            position = request.form['position']
            regno = request.form['registrationNo']

            user = getvoter(regno)
            
            if user:
                positionId = getpostid(position)
                msg = "Record successfully fetched."

                # name = user.name
                # regNo = user.regNo
                # email=  user.email
                # password= user.password
                # college = user.college
                # school= user.school
                # course= user.course
                # campus= user.campus
                # academicYear= user.academicYear
                # userIdNo= user.userIdNo
                name = user['name']
                regNo = user['regNo']
                email=  user['email']
                password= user['password']
                college = user['college']
                school= user['school']
                course= user['course']
                campus= user['campus']
                academicyear= user['academicYear']
                userIdNo= user['idNo']

                
                cur = conn.cursor()
                cur.execute("INSERT INTO candidates (name, regNo, college, academicYear, electedPost,idNo,email,school,course,campus) VALUES (?,?, ?, ?, ?, ?,?,?,?,?)", (name, regno, college, academicyear, positionId,userIdNo,email,school,course,campus))
                conn.commit()
                msg = "New Candidate successfully added"
                flash(message=msg, category='success')

            else:
                error = "Voter not found with the given registration number."
                flash(message=error, category='error')
                current_app.logger.error(error)
            return redirect(url_for('home'))
        except Exception as e:
            conn.rollback()
            error = f"Error in insert operation: {str(e)}"
            flash(message=error, category='error')
            current_app.logger.error(error, exc_info=True)
        finally:
            conn.close()

    return render_template('admin_candidate.html', posts=posts, msg=msg, error=error)


#Edit a candidate data
@app.route('/editcandidate/<reg_no>', methods=['GET', 'POST'])
def editcandidate(regno):
    if request.method == 'POST':
        try:
            name = request.form['name']
            reg_no = request.form['regNo']
            college = request.form['college']
            acad_year = request.form['academicYear']
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
            reg_no = request.form['regNo']

            self.get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM candidates WHERE regNo=?", (regno))
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

# #The electionvotes
# def electionvotes():
#     cursor = get_db_connection().cursor()
#     cursor.execute('SELECT * FROM candidates')
#     rows = cursor.fetchall()
   
#     return  rows

@app.route('/voting/<votePost>')
def voting(votePost):
    # votePost = votePost.lower()
    votePost = ' '.join(word.title() for word in votePost.split())
    votePostId = get_post_id(votePost)
    candidates = getCandidates_in_post(votePostId)
    candidates = [dict(candidate) for candidate in candidates]
    for candidate in candidates:
        if candidate['votes'] == None:
            candidate['votes'] = 0

    return render_template('voting_page.html',candidates = candidates, votePost=votePost)

def getCandidates_in_post(post):
    conn = get_db_connection()
    # positionName = getposition(post_id)
    candidates = conn.execute('SELECT * FROM candidates WHERE electedPost = ?', (post,)).fetchall()
    conn.close()
    return candidates

def get_post_id(post):
    conn = get_db_connection()
    post_id = conn.execute('SELECT id FROM posts WHERE name = ?', (post,)).fetchone()
    conn.close()
    return post_id['id'] if post_id else None

@app.route('/vote/<position>')
def vote_for_position(position):
    positionCandidates = get_candidates_for_position(position)

    return render_template('position_template.html', position=position, candidates=positionCandidates)

@app.route('/results')
def results():
    electedcandidates = getcandidates()
    if electedcandidates:
        return render_template('results.html', electedcandidates=electedcandidates)

    else:
        return render_template('results.html', electedcandidates="No Data Found")
    # electedcandidates = electionvotes()

    # # Check if there are any positions with elected candidates
    # if electedcandidates:
    #     return render_template('results.html', electedcandidates=electedcandidates)
    # else:
    #     # Handle the case where no data is found differently
    #     return render_template('results.html', nodata=True)
# #The results Page
# @app.route('/results')
# def results():
#     electedcandidates = electionvotes()
#     if len(electedcandidates) > 1:
#         return render_template('results.html', electedcandidates=electedcandidates)

#     else:
#         return render_template('results.html', electedcandidates="No Data Found")
     


@app.route('/vote_counts')
def vote_counts():
    cursor = get_db().cursor()
    cursor.execute('SELECT name, votes FROM candidates')
    rows = cursor.fetchall()
    return jsonify(rows)

# def electionvotes():
#     cursor = get_db_connection().cursor()
#     cursor.execute('SELECT * FROM candidates ORDER BY electedPost')
#     rows = cursor.fetchall()

#     # Group candidates by position
#     grouped_candidates = {}
#     for row in rows:
#         position = row['electedPost']
#         candidate = dict(row)
#         if position not in grouped_candidates:
#             grouped_candidates[position] = []
#         grouped_candidates[position].append(candidate)

#     return grouped_candidates

def electionvotes():
    cursor = get_db_connection().cursor()
    cursor.execute('SELECT * FROM candidates ORDER BY electedPost')
    rows = cursor.fetchall()

    grouped_candidates = {}
    for row in rows:
        position = row['electedPost']
        candidate = dict(row)
        if position not in grouped_candidates:
            grouped_candidates[position] = []
        grouped_candidates[position].append(candidate)

    return grouped_candidates if grouped_candidates else {}

    # Group candidates by position
    # grouped_candidates = {}
    # for row in rows:
    #     position = row['electedPost']
    #     candidate = dict(row)
    #     if position not in grouped_candidates:
    #         grouped_candidates[position] = []
    #     grouped_candidates[position].append(candidate)

    # return grouped_candidates


#Getting data from the databases

#Get the candidate data based on regNo

def getcandidates():
    conn = get_db_connection()
    candidates = conn.execute('SELECT * FROM candidates').fetchall()
    conn.close()
    # Convert sqlite3.Row objects to dictionaries
    #get the candidates position name
    
    candidates_list = [dict(candidate) for candidate in candidates]
    positions = get_posts()
    for candidate in candidates_list:
        position_id = candidate['electedPost']
        position_name = next((p['name'] for p in positions if p['id'] == position_id), None)
        candidate['electedPost'] = position_name


    return candidates_list
def get_posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return posts

def getposition(id):
    conn = get_db_connection()
    position = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    conn.close()
    return position

def getcandidatefromvoters(regno):
    conn = get_db_connection()
    candidate = conn.execute('SELECT * FROM voters WHERE regNo = ?', (regno,)).fetchone()
    conn.close()
    return candidate

def getcandidate(idNo):
    conn = get_db_connection()
    candidate = conn.execute('SELECT * FROM voters WHERE idNo = ?', (idNo,)).fetchone()
    conn.close()
    return candidate

def getvoter(regno):
    conn = get_db_connection()
    voter = conn.execute('SELECT * FROM voters WHERE regNo = ?', (regno,)).fetchone()
    conn.close()
    return dict(voter) if voter else None

def getpostid(name):
    conn = get_db_connection()
    postid = conn.execute('SELECT id FROM posts WHERE name = ?', (name,)).fetchone()
    conn.close()
    return postid['id'] if postid else None

def getCampuses():
    conn = get_db_connection()
    encrypted_campuses = conn.execute('SELECT name FROM campuses').fetchall()
    conn.close()
    return encrypted_campuses


def getColleges():
    conn = get_db_connection()
    encrypted_colleges = conn.execute('SELECT DISTINCT college FROM courseGrouped').fetchall()
    conn.close()
    return encrypted_colleges
    # decrypted_colleges = [decrypt_data(college['college']) for college in encrypted_colleges]
    # return decrypted_colleges

def getSchools(college):
    conn = get_db_connection()
    schools = conn.execute('SELECT DISTINCT  school FROM courseGrouped WHERE college = ?',(college,)).fetchall()
    conn.close()
    return schools

    # encrypted_schools = conn.execute('SELECT DISTINCT  school FROM courseGrouped WHERE college = ?',(encrypt_data(college),)).fetchall()
    # conn.close()
    # decrypted_schools = [decrypt_data(school['school']) for school in encrypted_schools]
    # return decrypted_schools

def getCourses(school):
    conn = get_db_connection()
    courses = conn.execute('SELECT DISTINCT course FROM courseGrouped WHERE school = ?',(school,)).fetchall()
    conn.close()
    return courses
    # decrypted_courses = [decrypt_data(course['course']) for course in courses]
    # return decrypted_courses

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

@app.route('/get_candidate_data', methods=['GET'])
def get_candidate_data():
    id_no = request.args.get('idNo')
    candidate_data = getcandidate(id_no)

    # Convert Row object to dictionary
    candidate_dict = dict(candidate_data)

    return jsonify(candidate_dict)


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
        return None
    except InvalidToken as inv:
        return inv
    except Exception as e:
        return e

def get_school_initials(school):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT initials FROM schools WHERE name = ?', (school,))
    result = cursor.fetchone()
    conn.close()

   # Extract the value from the row
    initials = result['initials'] if result else None

    return initials


def get_last_registration_number(school):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Assuming you have a table named 'registrations' with a column 'registration_number'
    query = 'SELECT regNo FROM voters WHERE school = ? ORDER BY regNo DESC LIMIT 1'
    result = cursor.execute(query, (school,)).fetchone()

    conn.close()
    

    # Return the last registration number or None if not found
    return result[0] if result else None

def get_next_registration_number(school):
    last_registration_number = get_last_registration_number(school)
    schoolinit = get_school_initials(school)


    if last_registration_number:
        match = re.search(r'(\d+/\d+)', last_registration_number)
        if match:
            numeric_part = int(match.group(1).split('/')[0])
            yr = last_registration_number[-4:]
            new_numeric_part = numeric_part + 1
            new_registration_number = re.sub(r'\d+/\d+', f'{new_numeric_part:04d}/{yr}', last_registration_number)
            return new_registration_number

    return f"{schoolinit}000-001/2023"

@app.route('/get_registration_number')
def get_registration_number():
    # Assuming you have a function to get the selected school from the form
    selected_school = request.args.get('school')

    # Get the next registration number based on the last registration number of the selected school
    next_registration_number = get_next_registration_number(selected_school)

    return jsonify({'registration_number': next_registration_number})

def get_selected_school():
    return request.args.get('school')




if __name__ == '__main__':
    app.run(debug=True) #debug=True is optional


