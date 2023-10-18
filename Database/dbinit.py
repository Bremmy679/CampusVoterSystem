import sqlite3
import random
from werkzeug.security import generate_password_hash, check_password_hash
import os
from faker import Faker

fake = Faker()

class Student:
    def __init__(self,name,regNo,email,password,college,school,campus,academicYear):
        self.name = name
        self.regNo = regNo
        self.email = email
        self.password = password
        self.college = college
        self.school = school
        self.campus = campus
        self.academicYear = academicYear

colleges = ["COPAS", "COHRED", "COETEC", "COANRE"]
academic_years = [1, 2, 3, 4, 5, 6]
prefix = random.choice(["SCT", "HRD"])

students = []

for _ in range(30):
    name = fake.name()
    reg_no = F'{prefix} {random.randint(100, 999)}-{random.randint(1000, 9999)}/{random.randint(2017, 2022)}'
    email = fake.email()
    password = fake.password()
    college = random.choice(colleges)
    school = "Computer Science"  # Assuming a default value
    campus = "Main"  # Assuming a default value
    academic_year = random.choice(academic_years)

    student_instance = Student(name, reg_no, email, password, college, school, campus, academic_year)
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
        cursor.execute(f"INSERT INTO candidates (name,regNo,email,password,college,school,campus,academicYear) VALUES (?,?,?,?,?,?,?,?)",
        (student.name,student.regNo,student.email,generate_password_hash(student.password),student.college,student.school,student.campus,student.academicYear))

    cursor.close()

    connection.commit()
    connection.close()


init_db()



# #define the students data


# students = [
#     Student('John Doe','SCT211-0011/2017','johndoe17@gmail.com','password123','School of Computing and Informatics','School of Computing and Informatics','Main Campus','2017'),
#     Student('Rose Waeni','SCT215-0012/2017','rosewaeni@gmail.com','password123','School of Computing and Informatics','School of Computing and Informatics','Main Campus','2017'),
# ]