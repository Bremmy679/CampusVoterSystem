DROP TABLE IF EXISTS candidates;
DROP TABLE IF EXISTS voters;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS campuses;
DROP TABLE IF EXISTS colleges;
DROP TABLE IF EXISTS schools;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS courseGrouped;


CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    regNo TEXT NOT NULL UNIQUE,  -- Assuming regNo uniquely identifies a candidate
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    college TEXT NOT NULL,
    school TEXT NOT NULL,
    course TEXT NOT NULL,
    campus TEXT NOT NULL,
    academicYear INTEGER NOT NULL,
    electedPost_id INTEGER,
    votes INTEGER,
    FOREIGN KEY (electedPost_id) REFERENCES posts(id),
    FOREIGN KEY (regNo) REFERENCES voters(regNo)  -- Reference the regNo field in voters
    FOREIGN KEY (campus) REFERENCES campuses(name)
    FOREIGN KEY (college) REFERENCES colleges(name)
    FOREIGN KEY (school) REFERENCES schools(name)
    FOREIGN KEY (course) REFERENCES courses(name)

);

CREATE TABLE voters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    regNo TEXT NOT NULL UNIQUE,  -- Assuming regNo uniquely identifies a voter
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    college TEXT NOT NULL,
    course TEXT NOT NULL,
    school TEXT NOT NULL,
    campus TEXT NOT NULL,
    academicYear INTEGER NOT NULL,
    idNo TEXT NOT NULL UNIQUE,
    FOREIGN KEY (campus) REFERENCES campuses(name)
    FOREIGN KEY (college) REFERENCES colleges(name)
    FOREIGN KEY (school) REFERENCES schools(name)
    FOREIGN KEY (course) REFERENCES courses(name)

);


CREATE TABLE campuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE colleges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE schools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE courseGrouped (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    college TEXT NOT NULL,
    school TEXT NOT NULL,
    course TEXT NOT NULL
);

/*
The various contested posts
*/

INSERT INTO posts (name) VALUES 
('President'), ('Vice President'), ('Secretary'), ('Treasurer'), ('Academic Secretary'), ('Accomodation Secretary');


/*
JKUAT Campuses
*/
INSERT INTO campuses (name) VALUES 
('Main Campus'), 
('Karen Campus'), 
('Westlands Campus'), 
('Kisii CBD Campus'), 
('Kisumu CBD Campus'), 
('Kitale CBD Campus'), 
('Nakuru CBD Campus'), 
('Mombasa CBD Campus');

-- /*
-- JKUAT Colleges
-- */
-- INSERT INTO colleges (name) VALUES 
-- ('College of Engineering and Technology'), 
-- ('College of Pure and Applied Sciences'), 
-- ('College of Health Sciences'), 
-- ('College of Human Resource Development'), 
-- ('College of Agriculture and Natural Resources Management'), 
-- ('College of Computing and Information Sciences'), 
-- ('College of Graduate Studies and Research');

-- /*
-- JKUAT Schools
-- */
-- INSERT INTO schools (name) VALUES 
-- ('School of Computing and Information Technology'), 
-- ('School of Biosystems and Environmental Engineering'), 
-- ('School of Biomedical Sciences and Technology'), 
-- ('School of Food and Nutrition Sciences'), 
-- ('School of Mathematical Sciences'), 
-- ('School of Civil, Environmental and Geospatial Engineering'), 
-- ('School of Electrical, Electronic and Information Engineering'), 
-- ('School of Mechanical, Manufacturing and Materials Engineering'), 
-- ('School of Architecture and Building Sciences'),
-- ('School of Agriculture and Enterprise Development'),
-- ('School of Pharmacy'),
-- ('School of Law'),
-- ('School of Business'),
-- ('School of Economics'),
-- ('School of Education'),
-- ('School of Physical Sciences'),
-- ('School of Medicine');

-- /*
-- JKUAT Courses
-- */
-- INSERT INTO courses (name) VALUES 
-- ('BSc. Computer Science'), 
-- ('BSc. Information Technology'), 
-- ('BSc. Information Technology (Evening)'), 
-- ('BSc. Computer Technology'),
-- ('Bachelor of Science in Agricultural Economics and Rural Development'),
-- ('Bachelor of Science in Agribusiness Management'),
-- ('Bachelor of Science in Animal Health, Production, and Processing'),
-- ('Bachelor of Architecture'),
-- ('Bachelor of Landscape Architecture'),
-- ('Bachelor of Science in Biosystems and Agricultural Engineering'),
-- ('Bachelor of Science in Environmental and Bio-Systems Engineering'),
-- ('Bachelor of Commerce'),
-- ('Bachelor of Business Information Technology'),
-- ('Bachelor of Purchasing and Supplies Management'),
-- ('Bachelor of Science in Civil Engineering'),
-- ('Bachelor of Science in Geospatial Engineering'),
-- ('Bachelor of Science in Computer Science'),
-- ('Bachelor of Science in Information Technology'),
-- ('Bachelor of Economics'),
-- ('Bachelor of Science in Electrical and Electronic Engineering'),
-- ('Bachelor of Science in Telecommunication and Information Engineering'),
-- ('Bachelor of Science in Mechanical Engineering'),
-- ('Bachelor of Science in Mechatronic Engineering'),
-- ('Bachelor of Science in Manufacturing Engineering'),
-- ('Bachelor of Science in Medical Laboratory Sciences'),
-- ('Bachelor of Science in Nursing'),
-- ('Bachelor of Science in Public Health'),
-- ('Bachelor of Science in Clinical Medicine'),
-- ('Bachelor of Science in Environmental Health'),
-- ('Bachelor of Science in Nutrition and Dietetics'),
-- ('Bachelor of Science in Food Science and Technology'),
-- ('Bachelor of Science in Mathematics and Computer Science'),
-- ('Bachelor of Science in Mathematics and Actuarial Science'),
-- ('Bachelor of Science in Mathematics and Economics'),
-- ('Bachelor of Science in Mathematics and Statistics'),
-- ('Bachelor of Science in Statistics and Programming'),
-- ('Bachelor of Science in Statistics and Actuarial Science'),
-- ('Bachelor of Science in Statistics and Economics'),
-- ('Bachelor of Science in Statistics and Computer Science'),
-- ('Bachelor of Science in Statistics and Finance'),
-- ('Bachelor of Science in Statistics and Mathematics'),
-- ('Bachelor of Science in Applied Statistics with Computing'),
-- ('Bachelor of Science in Actuarial Science'),
-- ('Bachelor of Science in Financial Engineering'),
-- ('Bachelor of Science in Mathematics'),
-- ('Bachelor of Science in Physics'),
-- ('Bachelor of Science in Physics and Computer Science'),
-- ('Bachelor of Science in Physics and Electronics'),
-- ('Bachelor of Science in Physics and Instrumentation'),
-- ('Bachelor of Science in Physics and Renewable Energy'),
-- ('Bachelor of Science in Physics and Nanotechnology'),
-- ('Bachelor of Science in Physics and Meteorology'),
-- ('Bachelor of Science in Physics and Space Science'),
-- ('Bachelor of Science in Chemistry'),
-- ('Bachelor of Science in Chemistry and Biology'),
-- ('Bachelor of Science in Chemistry and Mathematics'),
-- ('Bachelor of Science in Food Science and Nutrition');


INSERT INTO courseGrouped(college,school,course) VALUES
-- College of Agriculture and Natural Resources Management (CANREM)

('CANRE','School of Agriculture and Food Security', 'Bachelor of Science in Agricultural Economics and Rural Development'),
('CANRE', 'School of Agriculture and Food Security', 'Bachelor of Science in Agribusiness Management'),
('CANRE', 'School of Bioprocessing and Food Technology', 'Bachelor of Science in Food Science and Nutrition'),
-- College of Engineering and Technology (COETEC)

('COETEC', 'School of Civil, Environmental and Geospatial Engineering', 'Bachelor of Science in Civil Engineering'),
('COETEC', 'School of Electrical, Electronic and Information Engineering', 'Bachelor of Science in Electrical and Electronic Engineering'),
('COETEC', 'School of Mechanical, Manufacturing and Materials Engineering', 'Bachelor of Science in Mechanical Engineering'),

-- College of Pure and Applied Sciences (COPAS)

('COPAS', 'School of Computing and Information Technology', 'Bachelor of Science in Computer Science'),
('COPAS', 'School of Biological Sciences', 'Bachelor of Science in Biotechnology'),
('COPAS', 'School of Mathematical Sciences', 'Bachelor of Science in Actuarial Science'),
('COPAS', 'School of Computing and Information Technology', 'Bachelor of Science in Computer Science'),
('COPAS', 'School of Computing and Information Technology', 'Bachelor of Science in Information Technology'),
('COPAS', 'School of Computing and Information Technology', 'Bachelor of Science in Information Technology (Evening)'),
('COPAS', 'School of Computing and Information Technology', 'Bachelor of Science in Computer Technology'),
-- College of Health Sciences (COHES)

('COHES', 'School of Pharmacy', 'Bachelor of Pharmacy'),
('COHES', 'School of Public Health', 'Bachelor of Science in Public Health'),
('COHES', 'School of Nursing', 'Bachelor of Science in Nursing'),
-- College of Human Resource Development (COHRD)

('COHRED', 'School of Business', 'Bachelor of Commerce'),
('COHRED', 'School of Human Resource Development', 'Bachelor of Science in Human Resource Management'),
('COHRED', 'School of Entrepreneurship', 'Bachelor of Purchasing and Supplies Management');


/*The database schema*/

-- DROP TABLE IF EXISTS candidates;

-- CREATE TABLE candidates(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     name TEXT NOT NULL,
--     regNo TEXT NOT NULL,
--     email TEXT NOT NULL,
--     password TEXT NOT NULL,
--     college TEXT NOT NULL,
--     school TEXT NOT NULL,
--     campus TEXT NOT NULL,
--     academicYear INTEGER NOT NULL,
--     position TEXT,
--     electedPost TEXT,
--     votes INTEGER
-- );
    
