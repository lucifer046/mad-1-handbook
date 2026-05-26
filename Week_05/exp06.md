## Project Structure
```text
experiment-flask-sqlalchemy/
 main.py
 templates
     articles.html
     articles_by_author.html
```

---

# Experiment 06: Flask-SQLAlchemy
This experiment moves from pure SQLAlchemy to `Flask-SQLAlchemy`, which integrates the ORM directly into the Flask application lifecycle.

## Detailed Code Breakdown

### 1. Flask Integration
* `f_app.config['SQLALCHEMY_DATABASE_URI']`: This tells Flask exactly where our database file is located.
* `db = SQLAlchemy()`: We initialize the database object.
* `db.init_app(f_app)`: This links the database to our specific Flask app instance.
* `f_app.app_context().push()`: This is a critical step in Flask. It manually creates an "Application Context", allowing us to interact with the database (like creating tables) even outside of a web request.

### 2. Simplified Model Definitions
* Notice how we use `db.Model` and `db.Column` instead of importing everything from pure SQLAlchemy. The Flask extension provides these convenient shortcuts.
* `u_id`, `u_name`, `email`: These define the user fields.
* `db.relationship`: Again, we define the link between articles and users.

### 3. High-Level Queries
* `Article.query.all()`: Flask-SQLAlchemy adds a `.query` property to our models, making it very easy to fetch data.
* `Article.query.filter(...)`: This uses the built-in filtering capability to find articles written by a specific author.

### 4. Route Handling
* `@f_app.route("/")`: The root route fetches all articles and passes them to the `articles.html` template.
* `render_template(..., articles=arts)`: This sends our database results to the Jinja2 engine to be rendered into HTML.
