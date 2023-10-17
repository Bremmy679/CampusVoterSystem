/*The database schema*/

DROP TABLE IF EXISTS candidates;

CREATE TABLE candidates(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    regNo TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    college TEXT NOT NULL,
    school TEXT NOT NULL,
    campus TEXT NOT NULL,
    academicYear INTEGER NOT NULL,
    position TEXT,
    electedPost TEXT,
    votes INTEGER
);


   