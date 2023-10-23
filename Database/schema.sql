DROP TABLE IF EXISTS candidates;
DROP TABLE IF EXISTS voters;
DROP TABLE IF EXISTS posts;


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
    campus TEXT NOT NULL,
    academicYear INTEGER NOT NULL,
    electedPost_id INTEGER,
    votes INTEGER,
    FOREIGN KEY (electedPost_id) REFERENCES posts(id),
    FOREIGN KEY (regNo) REFERENCES voters(regNo)  -- Reference the regNo field in voters
);

CREATE TABLE voters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    regNo TEXT NOT NULL UNIQUE,  -- Assuming regNo uniquely identifies a voter
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    college TEXT NOT NULL,
    school TEXT NOT NULL,
    campus TEXT NOT NULL,
    academicYear INTEGER NOT NULL,
    FOREIGN KEY (campus) REFERENCES campuses(name)
);


CREATE TABLE campuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

INSERT INTO posts (name) VALUES 
('President'), ('Vice President'), ('Secretary'), ('Treasurer'), ('Academic Secretary'), ('Accomodation Secretary');

INSERT INTO campuses (name) VALUES 
('Main Campus'), 
('Karen Campus'), 
('Westlands Campus'), 
('Kisii CBD Campus'), 
('Kisumu CBD Campus'), 
('Kitale CBD Campus'), 
('Nakuru CBD Campus'), 
('Mombasa CBD Campus');



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
    
