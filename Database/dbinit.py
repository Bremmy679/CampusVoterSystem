import sqlite3
import random
from werkzeug.security import generate_password_hash, check_password_hash
import os
from faker import Faker
from flask import jsonify

fake = Faker()

class Student:
    def __init__(self,idNo,name,regNo,email,password,college,school,course,campus,academicYear):
        self.idNo = idNo
        self.name = name
        self.regNo = regNo
        self.email = email
        self.password = password
        self.college = college
        self.school = school
        self.course = course
        self.campus = campus
        self.academicYear = academicYear

colleges = ["COPAS", "COHRED", "COETEC", "COANRE"]
academic_years = [1, 2, 3, 4, 5, 6]
prefix = ["SCT", "HRD","HDE"]
#The JKUAT campuses

campuses = ["Main Campus-Juja", "Karen Campus", "Kisii CBD Campus", "Nairobi CBD Campus", "Kakamega CBD Campus"]
schools = ['Computing','Engineering','Agriculture']
students = []

for _ in range(30):
    idno = random.randint(10000000, 99999999)
    name = fake.name()
    reg_no = F'{random.choice(prefix)} {random.randint(100, 999)}-{random.randint(1000, 9999)}/{random.randint(2017, 2022)}'
    email = fake.email()
    password = fake.password()
    college = random.choice(colleges)
    school = random.choice(schools)  # Assuming a default value
    campus = random.choice(campuses)  # Assuming a default value
    course = fake.job()
    academic_year = random.choice(academic_years)

    student_instance = Student(idno,name, reg_no, email, password, college, school,course, campus, academic_year)
    students.append(student_instance)
    

def init_db():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full path to 'schema.sql'
    schema_path = os.path.join(script_dir, 'schema.sql')

    connection = sqlite3.connect('electiondb.db')
    with open (schema_path) as f:
        connection.executescript(f.read())

    cursor = connection.cursor()
    for student in students:
        cursor.execute(f"INSERT INTO voters (idNo,name,regNo,email,password,college,school,campus,academicYear,course) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (student.idNo,student.name,student.regNo,student.email,generate_password_hash(student.password),student.college,student.school,student.campus,student.academicYear,student.course))

    cursor.close()

    connection.commit()
    connection.close()


init_db()


# #define the students data


# students = [
#     Student('John Doe','SCT211-0011/2017','johndoe17@gmail.com','password123','School of Computing and Informatics','School of Computing and Informatics','Main Campus','2017'),
#     Student('Rose Waeni','SCT215-0012/2017','rosewaeni@gmail.com','password123','School of Computing and Informatics','School of Computing and Informatics','Main Campus','2017'),
# ]