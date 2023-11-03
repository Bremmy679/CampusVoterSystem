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
    name TEXT NOT NULL,
    regNo TEXT NOT NULL UNIQUE,  -- Assuming regNo uniquely identifies a candidate
    email TEXT NOT NULL,
    college TEXT NOT NULL,
    school TEXT NOT NULL,
    course TEXT NOT NULL,
    campus TEXT ,
    academicYear INTEGER NOT NULL,
    electedPost INTEGER,
    votes INTEGER,
    idNo INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (electedPost) REFERENCES posts(name),
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
    name TEXT NOT NULL,
    initials TEXT NOT NULL
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



