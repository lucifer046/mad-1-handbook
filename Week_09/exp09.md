## Project Structure
```text
experiment-flask-setup-logging/
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

# Experiment 09: Flask Logging
This experiment focuses on **Observability**. We set up structured logging to track exactly what happens inside our application, which is essential for debugging in production environments.

## Detailed Code Breakdown

### 1. The `logging` Module
* `import logging`: This is a standard Python library, not specific to Flask.
* `logging.basicConfig(...)`: This is where we configure the "how" and "where" of our logs.
    * `filename='debug.log'`: All logs will be written to this file.
    * `level=logging.DEBUG`: We want to see everything (Debug, Info, Warning, Error, Critical).
    * `format=...`: We define a custom format that includes the timestamp, severity level, and the specific message.

### 2. Flask's Built-in Logger
* `app_inst.logger`: Every Flask app has a `.logger` object. By default, it sends messages to the terminal, but since we configured `logging.basicConfig`, it will also send them to `debug.log`.
* `app_inst.logger.error(...)`: Used for critical failures that stop the app.
* `app_inst.logger.info(...)`: Used for general events (e.g., "App setup complete").

### 3. Log Levels
* **DEBUG**: Low-level details (e.g., "Querying database...").
* **INFO**: Normal operation (e.g., "User logged in").
* **ERROR**: Something went wrong but the app is still running.
* **CRITICAL**: The app cannot continue.
