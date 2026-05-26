## Project Structure
```text
experiment-flask-fullstack-setup/
 application
    __init__.py
    config.py
    controllers.py
    database.py
    models.py
 local_run.sh
 local_setup.sh
 main.py
 templates
     articles.html
     articles_by_author.html
```

---

# Experiment 07: Flask Fullstack Setup
This experiment demonstrates a professional project structure using the **Application Factory** pattern. This separates configuration, database initialization, and route handling into distinct modules.

## Detailed Code Breakdown

### 1. Modular Imports
* `application.config`: We store our database paths and secret keys in a separate file. This allows us to easily switch between "Development" and "Production" settings.
* `application.database`: The `db` object is created in its own file to prevent circular imports (a common problem in Flask).

### 2. The `init_app()` Factory
* Instead of creating the app globally, we wrap it in a function. This makes the code more testable and organized.
* `app_inst.config.from_object(...)`: We load our settings from a Python class. This is much cleaner than hardcoding strings.
* `db.init_app(app_inst)`: We initialize our database extension.

### 3. Controller Loading
* `from application.controllers import *`: Notice this is at the bottom of the file! We do this to ensure that the `f_app` is fully initialized before we try to attach routes (controllers) to it.

### 4. Running the Server
* `f_app.run(host='0.0.0.0', port=8080)`: We run the server on port 8080. Using `0.0.0.0` ensures it is accessible from outside the local machine (useful for Replit or Docker).
