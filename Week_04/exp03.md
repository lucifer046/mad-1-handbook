## Project Structure
```text
experiment-simple-flask-app/
 application.py
 templates
     display_details.html
     get_details.html
```

---

# Experiment 03: Simple Flask App
This experiment introduces the **Flask** web framework and demonstrates the fundamental pattern of handling web requests.

## Detailed Code Breakdown

### 1. The Flask Instance
* `f_app = Flask(__name__)`: This creates our main application object. The `__name__` argument helps Flask find our templates and static files.

### 2. Routes and Methods
* `@f_app.route("/", methods=["GET", "POST"])`: This is a "Decorator". it tells Flask that the `index()` function should handle any traffic to the root URL (`/`).
* `methods=["GET", "POST"]`: We explicitly allow two types of HTTP requests:
    * **GET**: Used when the user first visits the page (asking for the form).
    * **POST**: Used when the user submits the form data.

### 3. Request Handling
* `request.method`: We check which method was used to decide what to do.
* `request.form['name']`: When the method is `POST`, we look inside the incoming request to find the form data submitted by the user.

### 4. Template Rendering
* `render_template("get_details.html")`: Instead of manually merging data (like in Exp 02), we use Flask's built-in function which automatically looks in the `templates/` folder and handles the rendering for us.
