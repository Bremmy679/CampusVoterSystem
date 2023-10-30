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

colleges = ["COANRE", "COHES", "COETEC", "COHRED", "COPAS"]
academic_years = [1, 2, 3, 4, 5, 6]
pref = [
    ("SCHOOL OF AGRICULTURE AND ENVIRONMENTAL SCIENCES","AGA"),
    ("SCHOOL OF FOOD SCIENCE AND NUTRITIONAL SCIENCES","AGF"),
    ("SCHOOL OF NATURAL RESOURCES AND ANIMAL SCIENCES","AGN"),
    ("SCHOOL OF BIOMEDICAL SCIENCES","HSB"),
    ("SCHOOL OF MEDICINE","HSM"),
    ("SCHOOL OF PUBLIC HEALTH","HSH"),
    ("SCHOOL OF NURSING","HSN"),
    ("SCHOOL OF PHARMACY","HSP"),
    ("SCHOOL OF ELECTRICAL, ELECTRONIC AND INFORMATION ENGINEERING","ENE"),
    ("SCHOOL OF CIVIL, ENVIRONMENTAL AND GEOSPATIAL ENGINEERING","ENC"),
    ("SCHOOL OF MECHANICAL, MANUFACTURING AND MATERIALS ENGINEERING","ENM"),
    ("SCHOOL OF BIOSYSTEMS AND ENVIRONMENTAL ENGINEERING","ENB"),
    ("SCHOOL OF ARCHITECTURE AND BUILDING SCIENCES","ABS"),
    ("SCHOOL OF BUSINESS AND ENTREPRENEURSHIP","HDE"),
    ("SCHOOL OF COMMUNICATION AND DEVELOPMENT STUDIES","HDC"),
    ("SCHOOL OF BIOLOGICAL SCIENCES","SCB"),
    ("SCHOOL OF MATHEMATICS AND PHYSICAL SCIENCES","SCP"),
    ("SCHOOL OF COMPUTING AND INFORMATION TECHNOLOGY","SCT"),
]
#The JKUAT campuses

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
    ('COANRE', 'SCHOOL OF AGRICULTURE AND ENVIRONMENTAL SCIENCES', 'Bachelor of Science in Agriculture'),
    ('COANRE', 'SCHOOL OF AGRICULTURE AND ENVIRONMENTAL SCIENCES', 'Bachelor of Science in Landscape Science and Environmental Management'),
    ('COANRE', 'SCHOOL OF AGRICULTURE AND ENVIRONMENTAL SCIENCES', 'Diploma in General Agriculture'),
    ('COANRE', 'SCHOOL OF AGRICULTURE AND ENVIRONMENTAL SCIENCES', 'Bachelor of Science in Horticulture'),
    ('COANRE', 'SCHOOL OF AGRICULTURE AND ENVIRONMENTAL SCIENCES', 'Bachelor of Science in Environmental Horticulture and Landscaping Technology'),
    ('COANRE', 'SCHOOL OF AGRICULTURE AND ENVIRONMENTAL SCIENCES', 'Bachelor of Science in Agribusiness Management and Enterprise Development (AMED)'),
    ('COANRE', 'SCHOOL OF AGRICULTURE AND ENVIRONMENTAL SCIENCES', 'Bachelor of Science in Agricultural Economics and Rural Development (AERD)'),
    ('COANRE', 'SCHOOL OF AGRICULTURE AND ENVIRONMENTAL SCIENCES', 'Bachelor of Science in Agribusiness Economics and Food Industry Management (AFIM)'),
    ('COANRE', 'SCHOOL OF FOOD SCIENCE AND NUTRITIONAL SCIENCES', 'Bachelor of Science in Food Science and Technology'),
    ('COANRE', 'SCHOOL OF FOOD SCIENCE AND NUTRITIONAL SCIENCES', 'Bachelor of Science in Food Science and Postharvest Technology'),
    ('COANRE', 'SCHOOL OF FOOD SCIENCE AND NUTRITIONAL SCIENCES', 'Bachelor of Science in Nutraceutical Science And Technology'),
    ('COANRE', 'SCHOOL OF FOOD SCIENCE AND NUTRITIONAL SCIENCES', 'Bachelor of Science in Food Science and Nutrition'),
    ('COANRE', 'SCHOOL OF FOOD SCIENCE AND NUTRITIONAL SCIENCES', 'Bachelor of Science in Food Service and Hospitality Management'),
    ('COANRE', 'SCHOOL OF FOOD SCIENCE AND NUTRITIONAL SCIENCES', 'Bachelor of Science in Human Nutrition and Dietetics'),
    ('COANRE', 'SCHOOL OF NATURAL RESOURCES AND ANIMAL SCIENCES', 'Bachelor of Science in Animal Health, Production and Processing'),
    ('COANRE', 'SCHOOL OF NATURAL RESOURCES AND ANIMAL SCIENCES', 'Bachelor of Science in Land Resource Planning and Management'),
    ('COANRE', 'SCHOOL OF NATURAL RESOURCES AND ANIMAL SCIENCES', 'Bachelor of Science in Leather Technology'),
    ('COANRE', 'SCHOOL OF NATURAL RESOURCES AND ANIMAL SCIENCES', 'Bachelor of Science in Wildlife Science and Management'),
    ('COANRE', 'SCHOOL OF NATURAL RESOURCES AND ANIMAL SCIENCES', 'Bachelor of Science in Livestock Product Processing and Technology'),
    ('COHES', 'SCHOOL OF BIOMEDICAL SCIENCES', 'Bachelor of Science in Biochemistry and Molecular Biology'),
    ('COHES', 'SCHOOL OF BIOMEDICAL SCIENCES', 'Bachelor of Science in Medical Biochemistry'),
    ('COHES', 'SCHOOL OF BIOMEDICAL SCIENCES', 'Bachelor of Science in Medical Microbiology'),
    ('COHES', 'SCHOOL OF BIOMEDICAL SCIENCES', 'Bachelor of Radiography'),
    ('COHES', 'SCHOOL OF BIOMEDICAL SCIENCES', 'Bachelor of Science in Medical Laboratory Sciences'),
    ('COHES', 'SCHOOL OF BIOMEDICAL SCIENCES', 'Bachelor of Science in Applied Bioengineering'),
    ('COHES', 'SCHOOL OF BIOMEDICAL SCIENCES', 'Bachelor of Science in Forensic Science'),
    ('COHES', 'SCHOOL OF BIOMEDICAL SCIENCES', 'Bachelor of Science in Medical Lab Sciences'),
    ('COHES', 'SCHOOL OF BIOMEDICAL SCIENCES', 'Bachelor of Science in Applied Bioengineering'),
    ('COHES', 'SCHOOL OF MEDICINE', 'Bachelor of Medicine and Bachelor of Surgery (MBChB)'),
    ('COHES', 'SCHOOL OF MEDICINE', 'Bachelor of Science in Clinical Medicine and Community Health'),
    ('COHES', 'SCHOOL OF MEDICINE', 'Bachelor of Science in Comprehensive Ophthalmology and Cataract Surgery'),
    ('COHES', 'SCHOOL OF MEDICINE', 'Bachelor of Science in Physiotherapy'),
    ('COHES', 'SCHOOL OF MEDICINE', 'Bachelor of Science in Occupational Therapy'),
    ('COHES', 'SCHOOL OF MEDICINE', 'Bachelor of Science in Medical Social Work'),
    ('COHES', 'SCHOOL OF MEDICINE', 'Diploma in Clinical Medicine'),
    ('COHES', 'SCHOOL OF MEDICINE', 'Diploma in HIV/AIDS Management and Counseling'),
    ('COHES', 'SCHOOL OF PUBLIC HEALTH', 'Bachelor of Science in Public Health'),
    ('COHES', 'SCHOOL OF PUBLIC HEALTH', 'Bachelor of Science in Community Health and Development'),
    ('COHES', 'SCHOOL OF PUBLIC HEALTH', 'Bachelor of Science in Health Records and Information Management'),
    ('COHES', 'SCHOOL OF NURSING', 'Bachelor of Science in Nursing'),
    ('COHES', 'SCHOOL OF PHARMACY', 'Bachelor of Pharmacy'),
    ('COETEC', 'SCHOOL OF ELECTRICAL, ELECTRONIC AND INFORMATION ENGINEERING', 'Bachelor of Science in Electrical and Electronic Engineering'),
    ('COETEC', 'SCHOOL OF ELECTRICAL, ELECTRONIC AND INFORMATION ENGINEERING', 'Bachelor of Science in Electronic and Computer Engineering'),
    ('COETEC', 'SCHOOL OF ELECTRICAL, ELECTRONIC AND INFORMATION ENGINEERING', 'Bachelor of Science in Telecommunication and Information Engineering'),
    ('COETEC', 'SCHOOL OF CIVIL, ENVIRONMENTAL AND GEOSPATIAL ENGINEERING', 'Bachelor of Science in Civil Engineering'),
    ('COETEC', 'SCHOOL OF CIVIL, ENVIRONMENTAL AND GEOSPATIAL ENGINEERING', 'Bachelor of Science in Geomatic Engineering and Geospatial Information Systems'),
    ('COETEC', 'SCHOOL OF CIVIL, ENVIRONMENTAL AND GEOSPATIAL ENGINEERING', 'Bachelor of Science in Geospatial Information Science (4 Year Program)'),
    ('COETEC', 'SCHOOL OF MECHANICAL, MANUFACTURING AND MATERIALS ENGINEERING', 'Bachelor of Science in Mechatronic Engineering'),
    ('COETEC', 'SCHOOL OF MECHANICAL, MANUFACTURING AND MATERIALS ENGINEERING', 'Bachelor of Science in Mechanical Engineering'),
    ('COETEC', 'SCHOOL OF MECHANICAL, MANUFACTURING AND MATERIALS ENGINEERING', 'Bachelor of Science in Marine Engineering'),
    ('COETEC', 'SCHOOL OF MECHANICAL, MANUFACTURING AND MATERIALS ENGINEERING', 'Bachelor of Science in Mining and Mineral Processing Engineering'),
    ('COETEC', 'SCHOOL OF BIOSYSTEMS AND ENVIRONMENTAL ENGINEERING', 'Bachelor of Science in Agricultural and Biosystems Engineering'),
    ('COETEC', 'SCHOOL OF BIOSYSTEMS AND ENVIRONMENTAL ENGINEERING', 'Bachelor of Science in Water and Environment Management (4-year Program)'),
    ('COETEC', 'SCHOOL OF BIOSYSTEMS AND ENVIRONMENTAL ENGINEERING', 'Bachelor of Science in Energy and Environmental Technology'),
    ('COETEC', 'SCHOOL OF BIOSYSTEMS AND ENVIRONMENTAL ENGINEERING', 'Bachelor of Science in Aquaculture Technology'),
    ('COETEC', 'SCHOOL OF ARCHITECTURE AND BUILDING SCIENCES', 'Bachelor of Architectural Studies/Bachelor of Architecture'),
    ('COETEC', 'SCHOOL OF ARCHITECTURE AND BUILDING SCIENCES', 'Bachelor of Landscape Architecture'),
    ('COETEC', 'SCHOOL OF ARCHITECTURE AND BUILDING SCIENCES', 'Bachelor of Construction Management'),
    ('COETEC', 'SCHOOL OF ARCHITECTURE AND BUILDING SCIENCES', 'Bachelor of Quantity Surveying'),
    ('COETEC', 'SCHOOL OF ARCHITECTURE AND BUILDING SCIENCES', 'Bachelor of Real Estate'),
    ('COETEC', 'SCHOOL OF ARCHITECTURE AND BUILDING SCIENCES', 'Diploma in Architecture'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Bachelor of Science in Human Resource Management'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Bachelor of Science in Entrepreneurship'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Bachelor of Science in Strategic Management'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Bachelor of Science in Project Management'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Bachelor of Science in Business Innovation and Technology Management'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Bachelor of Science in Public Administration and Leadership'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Bachelor of Science in Supply Chain Management (Options: Clearing and Forwarding, Transport and Logistics, Maritime and Shipping)'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Bachelor of Science in Economics'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Bachelor of Science in Banking and Finance'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Bachelor of Business Information Technology'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Bachelor of Commerce'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Bachelor of Business and Office Management'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Bachelor of Science in Procurement and Contract Management'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Diploma in Purchasing and Supplies Management'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Diploma in Human Resource Management'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Diploma in County Governance'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Diploma in Microfinance'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Diploma in Business Information Technology'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Diploma in Business Administration'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Diploma in Strategic Management'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Certificate in Business Administration'),
    ('COHRED', 'SCHOOL OF BUSINESS AND ENTREPRENEURSHIP', 'Certificate in County Governance'),
    ('COHRED', 'SCHOOL OF COMMUNICATION AND DEVELOPMENT STUDIES', 'Bachelor of Mass Communication'),
    ('COHRED', 'SCHOOL OF COMMUNICATION AND DEVELOPMENT STUDIES', 'Bachelor of Journalism'),
    ('COHRED', 'SCHOOL OF COMMUNICATION AND DEVELOPMENT STUDIES', 'Bachelor of Corporate Communication Management'),
    ('COHRED', 'SCHOOL OF COMMUNICATION AND DEVELOPMENT STUDIES', 'Bachelor of Development Studies'),
    ('COHRED', 'SCHOOL OF COMMUNICATION AND DEVELOPMENT STUDIES', 'Bachelor of Public Management and Development'),
    ('COHRED', 'SCHOOL OF COMMUNICATION AND DEVELOPMENT STUDIES', 'Bachelor of Community Development and Environment'),
    ('COHRED', 'SCHOOL OF COMMUNICATION AND DEVELOPMENT STUDIES', 'Bachelor of Public Management'),
    ('COHRED', 'SCHOOL OF COMMUNICATION AND DEVELOPMENT STUDIES', 'Diploma in Mass Communication'),
    ('COHRED', 'SCHOOL OF COMMUNICATION AND DEVELOPMENT STUDIES', 'Diploma in Public Relations'),
    ('COHRED', 'SCHOOL OF COMMUNICATION AND DEVELOPMENT STUDIES', 'Diploma in Community Development'),
    ('COHRED', 'SCHOOL OF COMMUNICATION AND DEVELOPMENT STUDIES', 'Certificate in French'),
    ('COHRED', 'SCHOOL OF COMMUNICATION AND DEVELOPMENT STUDIES', 'Certificate in German'),
    ('COHRED', 'SCHOOL OF COMMUNICATION AND DEVELOPMENT STUDIES', 'Certificate in Chinese'),
    ('COHRED', 'SCHOOL OF COMMUNICATION AND DEVELOPMENT STUDIES', 'Certificate in Japanese'),
    ('COPAS', 'SCHOOL OF BIOLOGICAL SCIENCES', 'Bachelor of Science in Microbiology'),
    ('COPAS', 'SCHOOL OF BIOLOGICAL SCIENCES', 'Bachelor of Science in Biotechnology'),
    ('COPAS', 'SCHOOL OF BIOLOGICAL SCIENCES', 'Bachelor of Science in Biological Sciences'),
    ('COPAS', 'SCHOOL OF BIOLOGICAL SCIENCES', 'Bachelor of Science in Genomic Sciences'),
    ('COPAS', 'SCHOOL OF BIOLOGICAL SCIENCES', 'Bachelor of Science in Environmental Science'),
    ('COPAS', 'SCHOOL OF BIOLOGICAL SCIENCES', 'Bachelor of Science in Fisheries and Aquaculture Sciences'),
    ('COPAS', 'SCHOOL OF BIOLOGICAL SCIENCES', 'Bachelor of Science in Zoology'),
    ('COPAS', 'SCHOOL OF BIOLOGICAL SCIENCES', 'Bachelor of Science in Applied Biology'),
    ('COPAS', 'SCHOOL OF BIOLOGICAL SCIENCES', 'Bachelor of Science in General'),
    ('COPAS', 'SCHOOL OF BIOLOGICAL SCIENCES', 'Bachelor of Science in Botany'),
    ('COPAS', 'SCHOOL OF BIOLOGICAL SCIENCES', 'Bachelor of Science in Crop Protection'),
    ('COPAS', 'SCHOOL OF MATHEMATICS AND PHYSICAL SCIENCES', 'Bachelor of Science in Industrial Chemistry'),
    ('COPAS', 'SCHOOL OF MATHEMATICS AND PHYSICAL SCIENCES', 'Bachelor of Science in Analytical Chemistry'),
    ('COPAS', 'SCHOOL OF MATHEMATICS AND PHYSICAL SCIENCES', 'Bachelor of Science in Control and Instrumentation'),
    ('COPAS', 'SCHOOL OF MATHEMATICS AND PHYSICAL SCIENCES', 'Bachelor of Science in Geophysics'),
    ('COPAS', 'SCHOOL OF MATHEMATICS AND PHYSICAL SCIENCES', 'Bachelor of Science in Renewable Energy and Environmental Physics'),
    ('COPAS', 'SCHOOL OF MATHEMATICS AND PHYSICAL SCIENCES', 'Bachelor of Science in Chemistry'),
    ('COPAS', 'SCHOOL OF MATHEMATICS AND PHYSICAL SCIENCES', 'Bachelor of Science in Physics'),
    ('COPAS', 'SCHOOL OF MATHEMATICS AND PHYSICAL SCIENCES', 'Bachelor of Science in Mathematics'),
    ('COPAS', 'SCHOOL OF MATHEMATICS AND PHYSICAL SCIENCES', 'Bachelor of Science in Mathematics and Computer Science'),
    ('COPAS', 'SCHOOL OF MATHEMATICS AND PHYSICAL SCIENCES', 'Bachelor of Science in Industrial Mathematics'),
    ('COPAS', 'SCHOOL OF MATHEMATICS AND PHYSICAL SCIENCES', 'Bachelor of Science in Actuarial Science'),
    ('COPAS', 'SCHOOL OF MATHEMATICS AND PHYSICAL SCIENCES', 'Bachelor of Science in Financial Engineering'),
    ('COPAS', 'SCHOOL OF MATHEMATICS AND PHYSICAL SCIENCES', 'Bachelor of Science in Biostatistics'),
    ('COPAS', 'SCHOOL OF MATHEMATICS AND PHYSICAL SCIENCES', 'Bachelor of Science in Statistics'),
    ('COPAS', 'SCHOOL OF MATHEMATICS AND PHYSICAL SCIENCES', 'Bachelor of Science in Operations and Research'),
    ('COPAS', 'SCHOOL OF COMPUTING AND INFORMATION TECHNOLOGY', 'Bachelor of Science in Computer Science'),
    ('COPAS', 'SCHOOL OF COMPUTING AND INFORMATION TECHNOLOGY', 'Bachelor of Science in Computer Technology'),
    ('COPAS', 'SCHOOL OF COMPUTING AND INFORMATION TECHNOLOGY', 'Bachelor of Science in Information Technology'),
    ('COPAS', 'SCHOOL OF COMPUTING AND INFORMATION TECHNOLOGY', 'Bachelor of Science in Business Computing'),
    ('COPAS', 'SCHOOL OF COMPUTING AND INFORMATION TECHNOLOGY', 'Diploma in Information Technology'),
    ('COPAS', 'SCHOOL OF COMPUTING AND INFORMATION TECHNOLOGY', 'Certificate in Information Technology'),
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