# SQL & Relational Databases

## 1. What is a Database?

Think of a database as a super-powered, multi-sheet **Excel workbook**:
- Each "sheet" is a **Table**
- Each "row" is a **Record** (one entry, like one student)
- Each "column" is a **Field** (one property, like the student's name)
- The Excel app that runs it is the **Database Engine** (e.g., SQLite, PostgreSQL)

### Spreadsheets vs. Relational Databases

| Feature | Spreadsheets (Excel / Sheets) | Relational Databases (SQL) |
| :--- | :--- | :--- |
| **Data Capacity** | Slower or crashes with millions of rows | Handles **millions** of rows without slowing down |
| **Concurrency** | Difficult multi-user simultaneous edits | Handles **concurrent** read/write operations securely |
| **Integrity Constraints** | Easy to enter corrupt or invalid cells | Strict schema rules, keys, and values validation |
| **Relationships** | Lookup formulas (`VLOOKUP`) are easily broken | Dynamic **JOINS** linked automatically |

---

## 2. SQL: The Language to Talk to Databases

**SQL** (Structured Query Language) is the standard language used to interact with relational databases. It reads almost like plain English:

```
English: "Give me all students whose marks are greater than 40"
SQL: SELECT * FROM Students WHERE marks > 40;

English: "Add a new student named Carol with marks 92"
SQL: INSERT INTO Students (name, marks) VALUES ('Carol', 92);
```

---

## 3. Data Relationships

In relational design, entities are connected using relationships based on **Primary Keys** and **Foreign Keys**:

*   **One-to-One (1:1)**: A unique relationship where an entity in Table A connects to exactly one entity in Table B.
    *   *Example*: A Student and their unique StudentID Card.
*   **One-to-Many (1:N)**: One record in Table A relates to multiple records in Table B, but each Table B record relates back to only one A record.
    *   *Example*: One Hostel housing multiple Students.
*   **Many-to-Many (M:N)**: Multiple records in Table A can relate to multiple records in Table B. This is implemented using a **junction/bridge table**.
    *   *Example*: Students enrolling in multiple Courses.

---

## 4. The Four Types of SQL Commands

### DDL — Data Definition Language (Building the Structure)
DDL defines the database schema and table skeletons.

```sql
-- Step 1: Create the Hostels table (must exist BEFORE Students, since Students reference it)
CREATE TABLE Hostels (
    hostel_id INTEGER PRIMARY KEY, -- Unique ID for each hostel. Auto-numbered.
    name VARCHAR(50) NOT NULL -- Name of the hostel. Cannot be empty.
);

-- Step 2: Create the Students table
CREATE TABLE Students (
    student_id INTEGER PRIMARY KEY, -- Unique student ID
    name VARCHAR(100) NOT NULL, -- Full name (max 100 chars)
    marks INTEGER DEFAULT 0, -- Marks (defaults to 0 if not given)
    hostel_id INTEGER, -- Which hostel are they in?

    -- This line LINKS hostel_id to the Hostels table
    FOREIGN KEY (hostel_id) REFERENCES Hostels(hostel_id)
);
```

### DML — Data Manipulation Language (Working with Data)
DML manages inserting, updating, and deleting records.

```sql
-- Adding data
INSERT INTO Hostels VALUES (1, 'Godavari');
INSERT INTO Hostels VALUES (2, 'Kaveri');
INSERT INTO Students VALUES (101, 'Alice', 85, 1); -- Alice is in Godavari (hostel 1)
INSERT INTO Students VALUES (102, 'Bob', 35, 2); -- Bob is in Kaveri (hostel 2)
INSERT INTO Students VALUES (103, 'Carol', 92, 1); -- Carol is also in Godavari

-- Changing data
UPDATE Students SET marks = 40 WHERE student_id = 102; -- Bob just passed the re-exam!

-- Removing data
DELETE FROM Students WHERE student_id = 103; -- Remove Carol
```

### DQL — Data Query Language (Retrieving Data)
Queries let you filter, sort, and gather calculations using `SELECT`.

```sql
-- SELECT all columns (*) from all students
SELECT * FROM Students;

-- SELECT with a condition (WHERE)
SELECT * FROM Students WHERE marks >= 40; -- Only passing students

-- SELECT with sorting
SELECT * FROM Students ORDER BY marks DESC; -- Highest marks first

-- SELECT with pattern matching (LIKE)
SELECT * FROM Students WHERE name LIKE 'A%'; -- Names starting with 'A' (% means wild card)

-- Aggregate calculations
SELECT COUNT(*) FROM Students; -- How many students are there?
SELECT AVG(marks) FROM Students; -- What is the average marks?
```

---

## 5. SQL Joins: Combining Multiple Tables

Joins query spanning details from multiple tables utilizing key relationships.

```sql
-- INNER JOIN: Returns only rows that match in BOTH tables
SELECT Students.name AS student_name, Hostels.name AS hostel_name
FROM Students
INNER JOIN Hostels ON Students.hostel_id = Hostels.hostel_id;
```

### Types of Joins Illustrated

*   **INNER JOIN**: Returns records that have matching values in both tables.
    *   *Table A*: `[1, 2, 3]`
    *   *Table B*: `[2, 3, 4]`
    *   *Result*: `[2, 3]`
*   **LEFT JOIN (LEFT OUTER JOIN)**: Returns ALL records from the left table, and the matched records from the right table. Fill unmatched columns with `NULL`.
    *   *Table A*: `[1, 2, 3]`
    *   *Table B*: `[2, 3, 4]`
    *   *Result*: `[1=NULL, 2, 3]`
*   **RIGHT JOIN (RIGHT OUTER JOIN)**: Returns ALL records from the right table, and the matched records from the left table. Fill unmatched left columns with `NULL`.

---

## 6. Relational (SQL) vs. NoSQL Databases

While relational databases use structured schemas and SQL queries, NoSQL databases offer a flexible, schemaless model.

| Feature | Relational Databases (SQL) | NoSQL Databases (Document) |
| :--- | :--- | :--- |
| **Data Model** | Structured tables (rows and columns) | Unstructured documents (JSON / BSON / Key-Value) |
| **Schema** | Rigid, predefined schema | Flexible, dynamic schema |
| **Examples** | SQLite, PostgreSQL, MySQL | MongoDB, CouchDB, Redis |
| **Best For** | High integrity, ACID compliance, complex Joins | Hierarchical structures, rapid prototyping, scale-out |

---

## 7. ACID Properties: Database Transactions Guarantee

To guarantee safety during database operations (e.g., transferring bank balances), databases enforce the **ACID** standards:

*   **Atomicity**: "All-or-Nothing". The transaction completes entirely or rolls back completely if any sub-operation fails.
*   **Consistency**: A transaction only transforms the database from one valid state to another, obeying all constraints (e.g., balance cannot go negative).
*   **Isolation**: Transactions run concurrently without interfering with each other's updates.
*   **Durability**: Once committed, changes are written to persistent disk and survive server power failures.

---

## 8. Full Python SQLite Example

```python
import sqlite3

# Connect to (or create) a database file
conn = sqlite3.connect("school.db")
cursor = conn.cursor() # The cursor is used to issue SQL queries

# DDL: Create tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        marks INTEGER DEFAULT 0
    )
""")

# DML: Insert some students
cursor.execute("INSERT INTO Students (name, marks) VALUES (?, ?)", ("Alice", 85))
cursor.execute("INSERT INTO Students (name, marks) VALUES (?, ?)", ("Bob", 35))
cursor.execute("INSERT INTO Students (name, marks) VALUES (?, ?)", ("Carol", 92))
conn.commit() # Save the transactions permanently to disk!

# DQL: Query the data
print("\n--- All Students ---")
for row in cursor.execute("SELECT * FROM Students"):
    print(f"ID: {row[0]}, Name: {row[1]}, Marks: {row[2]}")

print("\n--- Passing Students (marks >= 40) ---")
for row in cursor.execute("SELECT * FROM Students WHERE marks >= 40"):
    print(f"{row[1]}: {row[2]}")

conn.close()
```

> [!WARNING]
> **SQL Injection Hazard**: Never use Python string formatting (e.g., `f"INSERT INTO Users VALUES ('{name}')"`) to build queries. Always use parameterized queries with placeholder placeholders (`?`) to prevent structural database manipulation from user inputs.

---

## Glossary

| Term | Meaning |
| :--- | :--- |
| **Table** | Grid-based structural representation of data (rows and columns) |
| **Primary Key** | Column(s) uniquely identifying each record in a table |
| **Foreign Key** | A reference column linking to a Primary Key of another table |
| **Transaction** | A set of database operations performed as a single unit |
| **ACID** | Reliability properties: Atomicity, Consistency, Isolation, Durability |
| **Junction Table** | A table mapping Relationships in a Many-to-Many relationship structure |
| **NoSQL** | Schemaless database systems supporting document or key-value storage formats |
