# Flask Web Framework & Routing

## 1. What is Flask?

Imagine you want to open a shop. You need:
1.  A building (the web server)
2.  A counter where customers come to ask for things (the route)
3.  A person behind the counter who fulfills requests (the Python function)

**Flask** is a lightweight Python web framework (often called a **microframework**) designed to make building web applications simple, elegant, and highly customizable. It provides core routing and templating features by default, without forcing a rigid database structure or folder layout on the developer.

---

## 2. Your First Flask App: The Minimal Version

Let's build the simplest possible web server:

```python
# Step 1: Import Flask from the flask library
from flask import Flask

# Step 2: Create the application instance
# __name__ is a special Python variable representing the current module name.
# Flask uses this to know where to find templates, assets, and static files.
app = Flask(__name__)

# Step 3: Create a ROUTE
# A route links a specific URL endpoint to a Python view function.
@app.route('/') # The '/' decorator targets the homepage
def home():
    return "<h1>Hello, World!</h1><p>My first Flask app!</p>"

# Step 4: Start the server
if __name__ == '__main__':
    app.run(debug=True) # debug=True reloads the server on changes and shows nice error traces
```

### The `__name__` Variable & `__main__` Guard
*   **`__name__`**: In Python, when a script is executed directly, `__name__` is set to `"__main__"`. If the script is imported elsewhere as a module, `__name__` takes the filename's name.
*   **`if __name__ == "__main__":`**: Ensures that `app.run()` is only executed when the file is run directly, and not when imported into tests or WSGI production servers.

---

## 3. How to Run and Configure the Development Server

### Running the App via CLI
You can boot up your server using Flask's command-line interface. Set the application target via environment variables first:

#### macOS / Linux
```bash
export FLASK_APP=app.py
flask run --debug
```

#### Windows PowerShell
```powershell
$env:FLASK_APP = "app.py"
flask run --debug
```

#### Windows Command Prompt (CMD)
```cmd
set FLASK_APP=app.py
flask run --debug
```

#### Version Checking
Ensure you are running Flask 2.0+ by executing:
```bash
flask --version
```

#### Running on Custom Ports
To bypass conflicts on the default port `5000`:
```bash
flask run --port 4999
```

---

## 4. How Routing Works

A **route** connects a URL path to a Python function.

```
  ┌──────────────────┐               ┌───────────────────────────┐               ┌───────────────────────────┐
  │ User Visits URL  │ ────────────> │    Flask Matches Route    │ ────────────> │  View Function Executes   │
  ├──────────────────┤               ├───────────────────────────┤               ├───────────────────────────┤
  │ /                │               │ @app.route('/')           │               │ home()                    │
  │ /about           │               │ @app.route('/about')      │               │ about()                   │
  │ /student/42      │               │ @app.route('/student/<id>')│              │ show_student(id=42)       │
  └──────────────────┘               └───────────────────────────┘               └───────────────────────────┘
```

### Dynamic Routes (URL Parameters)
You can capture dynamic parts of the URL using angular brackets `<type:variable_name>`:

```python
@app.route('/student/<int:student_id>')
def show_student(student_id):
    # student_id is parsed directly as a Python integer
    return f"<h1>Profile page for Student #{student_id}</h1>"

@app.route('/user/<username>')
def show_user(username):
    # Defaults to a string parameter
    return f"<p>Hello, {username}!</p>"
```

### Handling HTTP Methods (GET & POST)
By default, routes only listen to `GET` requests. To handle forms and database submissions, specify `POST` in the route methods:

```python
from flask import request, render_template

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # User is navigating to the login page -> Show form
        return render_template('login.html')

    elif request.method == 'POST':
        # User submitted the form -> Process credentials
        username = request.form.get('username')
        password = request.form.get('password')
        return f"Logging in {username}..."
```

---

## 5. Flask Project Directory Structure

For assets, styles, and templates to load correctly, maintain this standard directory structure:

```
my-flask-app/
  ├── static/                 # Static assets served directly without processing
  │   ├── css/
  │   │   └── main.css        # Linked via url_for in templates
  │   └── images/
  │       └── logo.png
  ├── templates/              # HTML templates rendered by Jinja2
  │   ├── base.html           # Master layout
  │   ├── home.html
  │   └── course.html
  ├── app.py                  # Main controller logic (routes, config)
  └── requirements.txt        # Project dependencies
```

---

## 6. Templates with Jinja2: Decoupling Code from Markup

Writing raw HTML strings in Python functions quickly becomes unmaintainable. Instead, return separate HTML templates using `render_template`:

```python
# app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/president/<int:ordinal>')
def president(ordinal):
    pres_dict = {
        "name": "Droupadi Murmu",
        "office": "President of India",
        "ordinal": ordinal
    }
    # Pass variables, dictionaries, and ints directly into the template context
    return render_template('president.html', pres=pres_dict, ord=ordinal, title=pres_dict['office'])
```

```html
<!-- templates/president.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <!-- Link CSS dynamically using url_for -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ pres.name }}</h1>
    <p>Rank: {{ ord }}th {{ pres.office }}</p>
</body>
</html>
```

### Linking Static Files
Always use the `url_for` helper to reference static assets inside templates. This prevents broken paths when moving folders:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
<script src="{{ url_for('static', filename='js/app.js') }}"></script>
```

---

## 7. Form Submissions and redirect/url_for

When handling `POST` submissions, avoid returning raw text or rendering direct templates to prevent form resubmission errors during page refreshes (the **Post/Redirect/Get (PRG) Pattern**).

```python
from flask import Flask, request, redirect, url_for, render_template

@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_name = request.form.get('name')
        marks = int(request.form.get('marks', 0))

        # ... Save to Database ...

        # Redirection avoids duplicate data submission on browser page-refresh!
        return redirect(url_for('list_students'))

    return render_template('add_student.html')

@app.route('/students')
def list_students():
    return render_template('students.html')
```

> [!TIP]
> **Why `url_for` over hardcoded endpoints?**: `url_for('list_students')` takes the **view function name** as its argument. If you modify your route path from `@app.route('/students')` to `@app.route('/all-students')` later, `url_for` automatically resolves the new route without causing broken links in your app!

---

## Glossary

| Term | Meaning |
| :--- | :--- |
| **Microframework** | A lightweight web framework focused only on core system services (routing, templating) |
| **Route** | A mapping configuration connecting a URL request path to a Python function |
| **WSGI** | Web Server Gateway Interface. Standard specification for communication between Python apps and web servers |
| **`__name__`** | Special variable returning the name of the execution module |
| **`render_template`** | Flask function that reads, compiles, parses placeholders, and returns an HTML template |
| **`url_for`** | Generates dynamic paths using Python view function names |
| **`request`** | Thread-safe object carrying form details, HTTP headers, query string inputs from the client |
| **PRG Pattern** | Post/Redirect/Get design pattern protecting forms from duplicate data inputs |
