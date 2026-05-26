# MVC Architecture

## The Problem: Why Do We Need Architecture?

Imagine writing your first web app. It starts small:

```python
# Your first "working" app (50 lines of chaos)
def handle_request():
    import sqlite3
    conn = sqlite3.connect("students.db")
    students = conn.execute("SELECT * FROM students").fetchall()
    html = "<html><body><h1 style='color:red'>Students</h1>"
    for s in students:
        if s[2] > 40: # magic number! What is 40?
            html += f"<p>PASS: {s[1]}</p>"
        else:
            html += f"<p>FAIL: {s[1]}</p>"
    html += "</body></html>"
    conn.close()
    return html
```

This "works" for 50 lines. But at 500 lines, it becomes **Spaghetti Code** — impossible to understand, impossible to fix, impossible for a teammate to touch.

**MVC** is the solution.

---

## MVC: The Restaurant Analogy

The best way to understand MVC is to think of a restaurant:

```
  ┌─────────────────────────────────────────────────────────────────────────────────┐
  │                           THE MVC RESTAURANT ANALOGY                            │
  ├──────────────────────────┬──────────────────────────┬───────────────────────────┤
  │       DINING ROOM        │          WAITER          │          KITCHEN          │
  │          (VIEW)          │       (CONTROLLER)       │          (MODEL)          │
  ├──────────────────────────┼──────────────────────────┼───────────────────────────┤
  │ • The menu, tables, and  │ • Takes orders from view │ • Cooks food in kitchen   │
  │   decor (what user sees) │ • Coordinates M & V      │ • Manages database state  │
  │ • Never cooks food       │ • Never cooks or serves  │ • Never serves customers  │
  │ • Never takes orders     │ • Delivers results       │ • Never sits at tables    │
  └──────────────────────────┴──────────────────────────┴───────────────────────────┘
```

### The Strict Rules:

1. **Customers (users) only talk to the Waiter (Controller)**
2. **The Waiter only talks to the Kitchen (Model) and brings food to the Dining Room (View)**
3. **The Kitchen NEVER serves food directly to customers**
4. **The Dining Room NEVER goes into the kitchen**

---

## The Three Components in Detail

### 1. The MODEL — Your Data Manager

The Model is responsible for **everything related to data**:
- Reading data from the database
- Writing data to the database
- Validating data (e.g., "Is this a valid email?")
- Business rules (e.g., "Students cannot register if fees are unpaid")

```python
# MODEL: Only talks about data. No HTML. No printing.
class StudentModel:
    def __init__(self):
        self.students = [
            {"id": 1, "name": "Alice", "marks": 85},
            {"id": 2, "name": "Bob", "marks": 35},
        ]

    def get_all_students(self):
        """Returns the list of all students from the database."""
        return self.students

    def get_student_by_id(self, student_id):
        """Finds a specific student. Returns None if not found."""
        for s in self.students:
            if s["id"] == student_id:
                return s
        return None

    def is_passing(self, student_id):
        """Business rule: passing mark is 40."""
        student = self.get_student_by_id(student_id)
        if student:
            return student["marks"] >= 40
        return False
```

### 2. The VIEW — Your Display Layer

The View is responsible for **showing data to the user**. It ONLY displays what it is given. It never fetches data itself.

```python
# VIEW: Only knows how to display. No database. No logic.
class StudentView:
    def show_student_list(self, students):
        """Takes a list of students and builds the HTML display."""
        html = "<html><body><h1>Student Report</h1><ul>"
        for s in students:
            html += f"<li>{s['name']} - Marks: {s['marks']}</li>"
        html += "</ul></body></html>"
        return html

    def show_pass_fail(self, student_name, is_passing):
        """Displays result for ONE student."""
        status = "✅ PASS" if is_passing else "❌ FAIL"
        return f"<p>{student_name}: {status}</p>"
```

### 3. The CONTROLLER — The Traffic Director

The Controller **receives requests** and **coordinates** the Model and View:

```python
# CONTROLLER: The middleman. Calls Model AND View, but does neither job itself.
class StudentController:
    def handle_view_all_request(self):
        """
        User visits /students
        Controller's job:
        1. Ask Model for data
        2. Pass data to View
        3. Return the result
        """
        model = StudentModel()
        view = StudentView()

        # Step 1: Get data from Model
        all_students = model.get_all_students()

        # Step 2 & 3: Give data to View, return the HTML
        return view.show_student_list(all_students)

    def handle_result_request(self, student_id):
        """
        User visits /result/2
        """
        model = StudentModel()
        view = StudentView()

        student = model.get_student_by_id(student_id)
        is_passing = model.is_passing(student_id)

        return view.show_pass_fail(student["name"], is_passing)


# --- Simulate the app running ---
controller = StudentController()
print(controller.handle_view_all_request())
print(controller.handle_result_request(1)) # Alice
print(controller.handle_result_request(2)) # Bob
```

---

## The Complete MVC Flow (Step by Step)

```
  BROWSER                       CONTROLLER                       MODEL                     VIEW
     │                              │                              │                        │
     │  "GET /students"             │                              │                        │
     ├─────────────────────────────>│                              │                        │
     │                              │ 1. Receives request          │                        │
     │                              │ 2. get_all_students()        │                        │
     │                              ├─────────────────────────────>│                        │
     │                              │                              │ 3. Query Database      │
     │                              │                              │ 4. Returns data        │
     │                              │<─────────────────────────────┤                        │
     │                              │                              │                        │
     │                              │ 5. show_student_list(data)   │                        │
     │                              ├──────────────────────────────┼───────────────────────>│
     │                              │                              │                        │ 6. Builds HTML
     │                              │                              │                        │ 7. Returns string
     │                              │<─────────────────────────────┼────────────────────────┤
     │                              │                              │                        │
     │  8. Returns finished HTML    │                              │                        │
     │<─────────────────────────────┤                              │                        │
     ▼                              ▼                              ▼                        ▼
```

---

## CRUD: The Four Operations on Any Data

Every web app, no matter what it does, is performing one of four operations:

| CRUD | SQL Command | HTTP Method | Example |
|:---|:---|:---|:---|
| **C**reate | `INSERT` | `POST` | Signing up |
| **R**ead | `SELECT` | `GET` | Viewing your profile |
| **U**pdate | `UPDATE` | `PUT` | Changing your password |
| **D**elete | `DELETE` | `DELETE` | Removing a post |

[WARNING]
**Never mix layers!** The Controller should **never** write `SELECT * FROM students` directly. The Model does that. The View should **never** call the database. If you find yourself doing this, your architecture has a problem.
[/CALLOUT]

---

## Glossary

| Term | Meaning |
|:---|:---|
| **MVC** | Model-View-Controller — an architecture pattern for organizing code |
| **Model** | The layer that manages data and business rules |
| **View** | The layer that displays information to the user |
| **Controller** | The layer that connects Model and View, handles requests |
| **Business Logic** | The rules specific to your application (e.g., "passing mark is 40") |
| **Spaghetti Code** | Code where everything is tangled together with no clear structure |
| **CRUD** | The four fundamental data operations: Create, Read, Update, Delete |
