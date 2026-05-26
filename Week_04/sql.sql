-- SQL Schema and Queries Example

-- 1. Create Tables
CREATE TABLE Hostels (
    ID INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    capacity INTEGER
);

CREATE TABLE Students (
    IDNumber INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    hostelID INTEGER,
    FOREIGN KEY (hostelID) REFERENCES Hostels(ID)
);

CREATE TABLE Courses (
    ID INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT,
    year INTEGER
);

CREATE TABLE StudentCourses (
    studentID INTEGER,
    courseID INTEGER,
    marks INTEGER,
    PRIMARY KEY (studentID, courseID),
    FOREIGN KEY (studentID) REFERENCES Students(IDNumber),
    FOREIGN KEY (courseID) REFERENCES Courses(ID)
);

-- 2. Insert Data
INSERT INTO Hostels VALUES (1, 'Godavari', 500);
INSERT INTO Hostels VALUES (2, 'Cauvery', 400);

INSERT INTO Students VALUES (101, 'Alice', 1);
INSERT INTO Students VALUES (102, 'Bob', 2);

-- 3. Queries
-- Simple Select
SELECT name FROM Students WHERE IDNumber = 101;

-- Join Query: Find student name and their hostel name
SELECT Students.name, Hostels.name as hostel_name
FROM Students
INNER JOIN Hostels ON Students.hostelID = Hostels.ID;

-- Aggregate Query: Count students per hostel
SELECT hostelID, COUNT(*) as student_count
FROM Students
GROUP BY hostelID;

-- Pattern Matching
SELECT * FROM Students WHERE name LIKE 'A%';
