import sqlite3
import random
from werkzeug.security import generate_password_hash, check_password_hash
import os
from faker import Faker
from flask import jsonify
from cryptography.fernet import Fernet

fake = Faker()
key = Fernet.generate_key()
cipher_suite = Fernet(key)


def encrypt_data(data):
    encrypted_data = cipher_suite.encrypt(data.encode('utf-8'))
    return encrypted_data

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

for _ in range(2):
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
        (student.idNo),student.name,student.regNo,student.email,generate_password_hash(student.password),student.college,student.school,student.campus,student.academicYear,student.course)

    post_names = ['President', 'Vice President', 'Secretary', 'Treasurer', 'Academic Secretary', 'Accommodation Secretary']
    # encrypted_posts = [encrypt_data(name) for name in post_names]
    
    # Use placeholders for the values
    placeholders = ', '.join(['?' for _ in post_names])

    # Execute the query with placeholders and encrypted values
    cursor.executemany("INSERT INTO posts (name) VALUES (?)", [(post,) for post in post_names])


    # Example for campuses table
    campus_names = ['Main Campus', 'Karen Campus', 'Westlands Campus', 'Kisii CBD Campus', 'Kisumu CBD Campus', 'Kitale CBD Campus', 'Nakuru CBD Campus', 'Mombasa CBD Campus']
    cursor.executemany("INSERT INTO campuses (name) VALUES (?)", [(campus,) for campus in campus_names])
        # Encrypt the campus names
    # encrypted_campuses = [encrypt_data(name) for name in campus_names]

    # # Use placeholders for the values
    # placeholders = ', '.join(['?' for _ in campus_names])

    # Execute the query with placeholders and encrypted values
    # cursor.executemany("INSERT INTO campuses (name) VALUES (?)", [(campus,) for campus in encrypted_campuses])


    # cursor.execute("INSERT INTO posts (name) VALUES ('President'), ('Vice President'), ('Secretary'), ('Treasurer'), ('Academic Secretary'), ('Accomodation Secretary')")
    # cursor.execute("INSERT INTO campuses (name) VALUES ('Main Campus'), ('Karen Campus'), ('Westlands Campus'), ('Kisii CBD Campus'), ('Kisumu CBD Campus'), ('Kitale CBD Campus'), ('Nakuru CBD Campus'), ('Mombasa CBD Campus')")

    course_data = [
    ('CANRE', 'School of Agriculture and Food Security', 'Bachelor of Science in Agricultural Economics and Rural Development'),
    ('CANRE', 'School of Agriculture and Food Security', 'Bachelor of Science in Agribusiness Management'),
    ('CANRE', 'School of Bioprocessing and Food Technology', 'Bachelor of Science in Food Science and Nutrition'),
    ('COETEC', 'School of Civil, Environmental and Geospatial Engineering', 'Bachelor of Science in Civil Engineering'),
    ('COETEC', 'School of Electrical, Electronic and Information Engineering', 'Bachelor of Science in Electrical and Electronic Engineering'),
    ('COETEC', 'School of Mechanical, Manufacturing and Materials Engineering', 'Bachelor of Science in Mechanical Engineering'),
    ('COPAS', 'School of Computing and Information Technology', 'Bachelor of Science in Computer Science'),
    ('COPAS', 'School of Biological Sciences', 'Bachelor of Science in Biotechnology'),
    ('COPAS', 'School of Mathematical Sciences', 'Bachelor of Science in Actuarial Science'),
    ('COPAS', 'School of Computing and Information Technology', 'Bachelor of Science in Computer Science'),
    ('COPAS', 'School of Computing and Information Technology', 'Bachelor of Science in Information Technology'),
    ('COPAS', 'School of Computing and Information Technology', 'Bachelor of Science in Information Technology (Evening)'),
    ('COPAS', 'School of Computing and Information Technology', 'Bachelor of Science in Computer Technology'),
    ('COHES', 'School of Pharmacy', 'Bachelor of Pharmacy'),
    ('COHES', 'School of Public Health', 'Bachelor of Science in Public Health'),
    ('COHES', 'School of Nursing', 'Bachelor of Science in Nursing'),
    ('COHRED', 'School of Business', 'Bachelor of Commerce'),
    ('COHRED', 'School of Human Resource Development', 'Bachelor of Science in Human Resource Management'),
    ('COHRED', 'School of Entrepreneurship', 'Bachelor of Purchasing and Supplies Management')
    ]

    # # Encrypt the data
    # encrypted_course_data = [(encrypt_data(college), encrypt_data(school), encrypt_data(course)) for college, school, course in course_data]

    # # Prepare the SQL query
    placeholders = ', '.join(['?' for _ in course_data[0]])

    # # Execute the query with placeholders and encrypted values
    # cursor.executemany(f"INSERT INTO courseGrouped (college, school, course) VALUES ({placeholders})", encrypted_course_data)
    cursor.executemany(f"INSERT INTO courseGrouped(college,school,course) VALUES ({placeholders})", course_data)

    cursor.close()

    connection.commit()
    connection.close()


init_db()


#Data encrypter



# #define the students data


# students = [
#     Student('John Doe','SCT211-0011/2017','johndoe17@gmail.com','password123','School of Computing and Informatics','School of Computing and Informatics','Main Campus','2017'),
#     Student('Rose Waeni','SCT215-0012/2017','rosewaeni@gmail.com','password123','School of Computing and Informatics','School of Computing and Informatics','Main Campus','2017'),
# ]