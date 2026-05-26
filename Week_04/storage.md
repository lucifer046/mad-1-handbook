# Persistent Storage

## The Big Problem: Computers Have Amnesia

When your Python program runs, all variables live in **RAM** (Random Access Memory). The moment you close the program, the RAM is wiped clean. Everything is gone.

```
  ┌────────────────────────────────────────────────────────┐
  │ 🔌 Run Program:   student = "Alice"  (Stored in RAM)   │
  ├────────────────────────────────────────────────────────┤
  │ 🛑 Close Program: Poof! Gone forever. (RAM is cleared) │
  └────────────────────────────────────────────────────────┘
```

This is why we need **Persistent Storage** — a way to save data that survives program restarts.

---

## Types of Storage: From Fastest to Slowest

Think of it like where you keep things at home:

```
  ▲  SPEED & COST  │       [ THE STORAGE PYRAMID ]
  │    (Highest)   │
  │        ▲       │             ┌───────────┐
  │       ╱ ╲      │             │ REGISTERS │ (In CPU - instant access)
  │      ╱   ╲     │             ├───────────┤
  │     ╱     ╲    │             │    RAM    │ (Volatile - temporary work desk)
  │    ╱       ╲   │            ┌┴───────────┴┐
  │   ╱         ╲  │            │     SSD     │ (Non-volatile - permanent room bookshelf)
  │  ╱           ╲ │           ┌┴─────────────┴┐
  │ ╱             ╲│           │     HDD     │ (Magnetic platters - large filing cabinet)
  │ ───────────────│          ┌┴───────────────┴┐
  │    (Lowest)    │          │  COLD STORAGE  │ (Cloud archive - far away storage unit)
  ▼   SIZE & CAPACITY         └─────────────────┘
```

---

## Serialization: Converting Objects to Saveable Formats

Your Python code uses **objects** (like a `Student` class). But files only store **raw text or bytes**. Converting one to the other is called **Serialization**.

```
   ┌────────────────────────────────┐              Serialization             ┌────────────────────────┐
   │         PYTHON OBJECT          ├───────────────────────────────────────>│  FILE / NETWORK STREAM  │
   │  Student Class:                │                                        │ "Alice,21CS001,85"     │
   │    name = "Alice"              │<───────────────────────────────────────┤ (Raw text or bytes)    │
   │    roll = "21CS001"            │             Deserialization            └────────────────────────┘
   │    marks = 85                  │
   └────────────────────────────────┘

```

### Option 1: CSV Files (Comma Separated Values)

The simplest way to store tabular data. Any spreadsheet app can open it.

```
student_id,name,marks,hostel
101,Alice,85,Godavari
102,Bob,35,Kaveri
103,Carol,72,Yamuna
```

**Pros**: Human-readable, works in Excel/Sheets
**Cons**: No data types (everything is text), no relationships between data, gets slow with large files

### Option 2: Pickling (Python-Specific)

Python's `pickle` module converts any Python object directly to binary bytes.

```python
import pickle

# SAVING (Serializing)
student = {"name": "Alice", "marks": 85}
with open("student.pkl", "wb") as f: # wb = write binary
    pickle.dump(student, f)

# LOADING (Deserializing)
with open("student.pkl", "rb") as f: # rb = read binary
    loaded_student = pickle.load(f)

print(loaded_student) # {'name': 'Alice', 'marks': 85}
```

**Pros**: Super easy, preserves exact Python types
**Cons**: Only works in Python! Can't share with a website or Android app.

[WARNING]
**Security Risk**: NEVER unpickle data from an untrusted source (like the internet). Pickle files can contain malicious code that executes when you load them!
[/CALLOUT]

### Option 3: Relational Databases (The Professional Way)

For real applications, we use databases. A database is like a very smart Excel spreadsheet that can:
- Handle millions of rows without slowing down
- Link data across multiple "sheets" (tables)
- Allow many users to read/write simultaneously
- Guarantee data safety even if the server crashes

---

## Data Relationships: How Tables Link Together

In a school database, data is split across multiple tables. Tables are linked by **IDs**.

```
   ┌──────────────────────────────────────┐                   ┌───────────────────────────┐
   │           STUDENTS TABLE             │                   │       HOSTELS TABLE       │
   ├──────┬─────────┬─────────────────────┤                   ├──────┬────────────────────┤
   │  ID  │  Name   │  hostel_id [FK] ────┼──────────────────>│  ID  │  Name              │
   ├──────┼─────────┼─────────────────────┤                   ├──────┼────────────────────┤
   │  1   │  Alice  │  1                  │                   │  1   │  Godavari          │
   │  2   │  Bob    │  2                  │                   │  2   │  Kaveri            │
   │  3   │  Carol  │  1                  │                   └──────┴────────────────────┘
   └──────┴─────────┴─────────────────────┘
```

### Types of Relationships

```
  [ ONE-to-ONE RELATIONSHIP ]
  ┌───────────┐                1 : 1                ┌───────────────┐
  │  Student  ├─────────────────────────────────────┤  Roll Number  │
  └───────────┘                                     └───────────────┘

  [ ONE-to-MANY RELATIONSHIP ]
  ┌───────────┐                1 : N                ┌───────────────┐
  │  Hostel   ├──────────┬──────────────────────────┤   Student A   │
  └───────────┘          │                          ├───────────────┤
                         ├──────────────────────────┤   Student B   │
                         │                          ├───────────────┤
                         └──────────────────────────┤   Student C   │
                                                    └───────────────┘

  [ MANY-to-MANY RELATIONSHIP ]
  ┌───────────┐             1 : N         N : 1             ┌───────────────┐
  │  Student  ├───────────────> ┌─────────────┐ <───────────┤    Course     │
  └───────────┘                 │  JUNCTION   │             └───────────────┘
                                │    TABLE    │
                                └─────────────┘
```

---

## Relational vs. NoSQL: Choosing the Right Database

| Feature | Relational (SQL) | NoSQL |
|:---|:---|:---|
| **Structure** | Fixed tables and columns (like Excel) | Flexible (like JSON documents) |
| **Relationships** | Excellent, foreign keys | Weak, you manage it yourself |
| **Use When** | Data is structured and predictable | Data changes shape frequently |
| **Examples** | SQLite, PostgreSQL, MySQL | MongoDB, Firebase, Redis |
| **Analogy** | A well-organized filing cabinet | A pile of sticky notes |

---

## Glossary

| Term | Meaning |
|:---|:---|
| **Persistence** | Data that survives program restarts |
| **RAM** | Temporary, fast memory that is cleared on power off |
| **SSD/HDD** | Permanent storage (like a hard drive in your laptop) |
| **Serialization** | Converting a Python object into a saveable format |
| **CSV** | Comma-Separated Values — a plain text format for tabular data |
| **Pickle** | Python's built-in module for serializing Python objects to binary |
| **Primary Key** | A unique ID that identifies each row in a table |
| **Foreign Key** | A column that links two tables together |
| **Schema** | The formal definition of a database's table structure |
