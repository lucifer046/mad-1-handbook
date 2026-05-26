# Deployment and DevOps

## What is Deployment?

You've been coding on your laptop. Your app runs perfectly. But it only runs for YOU, on YOUR machine.

**Deployment** is the process of putting your app onto a server that is connected to the internet, so that **anyone in the world** can use it.

```
  [ YOUR LAPTOP ]             [ INTERNET ]             [ PRODUCTION SERVER ]
     (Only You)                                            (Running 24/7)
  ┌──────────────┐                                        ┌──────────────┐
  │  • app.py    │ ─────────► Deployment ───────────────► │  • app.py    │
  │  • style.css │                                        │  • style.css │
  └──────────────┘                                        └──────┬───────┘
                                                                 │
                                                                 ▼
                                                      Millions of visitors
                                                       can access your app!
```

---

## The Three Cloud Service Models

Think of building in the cloud like renting a kitchen:

```

                      WHAT YOU MANAGE vs. WHAT THEY MANAGE


  ┌──────────────────────────┬──────────────────────────┬───────────────────────────┐
  │           IaaS           │           PaaS           │           SaaS            │
  │ (Infrastructure-Service) │    (Platform-Service)    │    (Software-Service)     │
  ├──────────────────────────┼──────────────────────────┼───────────────────────────┤
  │ "Renting a raw plot"     │ "Renting a full kitchen" │ "Ordering restaurant food"│
  │                          │                          │                           │
  │ You Get:                 │ You Get:                 │ You Get:                  │
  │ • Raw virtual computer   │ • Platform pre-installed │ • A complete, ready-to-use│
  │ • Network interface      │   with Python runtime    │   finished software app   │
  │                          │                          │                           │
  │ You Manage:              │ You Manage:              │ You Manage:               │
  │ • OS updates, DB setup,  │ • Just your own Flask    │ • Nothing technical       │
  │   Flask/Python runtime   │   application code       │ • Only your user account  │
  │                          │                          │                           │
  │ Examples:                │ Examples:                │ Examples:                 │
  │ • AWS EC2, DigitalOcean  │ • Heroku, Render, Railway│ • Gmail, Google Docs      │
  └──────────────────────────┴──────────────────────────┴───────────────────────────┘


```

---

## CI/CD: Automating the Entire Pipeline

**Without CI/CD:**
```
  [ LEGACY MANUAL PIPELINE (Fragile & Error-Prone) ]
  Developer Code  ──►  Manual Tests  ──►  Manual Build  ──►  Manual Copy  ──►  Live Server (Hopefully!)

  [ MODERN CI/CD AUTOMATED PIPELINE (Robust & Secure) ]
  Developer Push  ──►  GitHub Actions (CI)  ──►  Automated Build  ──►  Auto-Deploy (CD)  ──►  Live Server
                        (Runs All Tests)         (If Tests Pass)       (Zero Downtime)      (Every Time!)
```

### A Real GitHub Actions Workflow File

This is the YAML file that automates everything:

```yaml
# .github/workflows/deploy.yml
name: Test and Deploy

on:
  push:
    branches: [ main ] # Trigger this when code is pushed to main branch

jobs:
  test:
    runs-on: ubuntu-latest # Run on a fresh Linux machine

    steps:
      - uses: actions/checkout@v2 # Step 1: Download your code

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt # Step 2: Install packages

      - name: Run tests
        run: pytest # Step 3: Run all tests!

      # If tests fail, everything STOPS HERE. No broken code gets deployed.

      - name: Deploy to server
        run: |
          # Step 4: If we reach here, all tests passed. Deploy!
          echo "Deploying to production..."
```

---

## Docker: "It Works on MY Machine" — Problem Solved

The most common phrase in software development is:

> **"But it works on MY machine!"**

This happens because your laptop has Python 3.11, your teammate has Python 3.8, and the server has Python 3.6. Different versions, different behaviors!

**Docker** solves this by bundling your entire app AND its environment into a single **container** — like a shipping container that carries everything needed.

```
            [ WITHOUT DOCKER (Dependency Chaos) ]
     Your Laptop          Teammate Laptop           Production Server
    ┌─────────────┐       ┌─────────────┐          ┌─────────────────┐
    │ Python 3.11 │       │ Python 3.8  │          │ Python 3.6      │
    │ Flask 2.0   │       │ Flask 1.5   │          │ (Outdated OS)   │
    ├─────────────┤       ├─────────────┤          ├─────────────────┤
    │  ✅ Works!  │       │ ❌ Broken!  │          │ 💥 Crashing!    │
    └─────────────┘       └─────────────┘          └─────────────────┘

            [ WITH DOCKER (Universal Container) ]
    ┌────────────────────────────────────────────────────────────────┐
    │                       DOCKER CONTAINER                         │
    │  • Fixed OS Context (Linux Slim)                               │
    │  • Frozen Python version (3.11)                                │
    │  • Locked dependency libraries (Flask 2.0)                     │
    ├────────────────────────────────────────────────────────────────┤
    │  Runs Identically On:   Laptop   ──►   Teammate   ──►   Server │
    │                         (100% Deterministic & Stable!)         │
    └────────────────────────────────────────────────────────────────┘
```

### A Dockerfile Example

```dockerfile
# Dockerfile — The "recipe" for building your Docker image

# Step 1: Start from an official Python image
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy your requirements file and install packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# Step 4: Copy all your app files into the container
COPY . .

# Step 5: Tell Docker how to RUN your app
CMD ["python", "app.py"]
```

```bash
# Build the image from your Dockerfile
docker build -t my-flask-app .

# Run your container (your app is now live on port 5000)
docker run -p 5000:5000 my-flask-app
```

---

## Logging: Your App's "Black Box Recorder"

An airplane has a "black box" that records everything. Your app needs logging for the same reason — to understand what went wrong when something crashes.

```
  2026-04-19 10:32:01 INFO → User alice logged in
  2026-04-19 10:32:15 INFO → GET /students - 200 OK (45ms)
  2026-04-19 10:32:20 WARNING → Database query took 3.2 seconds (slow!)
  2026-04-19 10:32:45 ERROR → Unhandled exception in /checkout
  2026-04-19 10:32:45 ERROR → ZeroDivisionError: division by zero
  2026-04-19 10:32:45 ERROR → File "app.py", line 87, in calculate_total
```

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, # Log INFO and above (not DEBUG)
    format='%(asctime)s %(levelname)s → %(message)s',
    filename='app.log' # Save to a file
)

logger = logging.getLogger(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')

    logger.info(f"Login attempt for user: {username}")

    if authenticate(username, request.form.get('password')):
        logger.info(f"Login SUCCESS for user: {username}")
        return redirect('/dashboard')
    else:
        logger.warning(f"Login FAILED for user: {username}")
        return "Invalid credentials", 401
```

### Log Levels (From Least to Most Severe)

```
  DEBUG → Very detailed. "I'm about to run this query..."
  INFO → Normal events. "User logged in."
  WARNING → Something unexpected but not breaking. "Slow query!"
  ERROR → Something broke. "Exception occurred."
  CRITICAL → The app itself is in trouble. "Cannot connect to database!"
```

[WARNING]
**Log Rotation**: Without it, your log files grow forever and eventually fill up the entire server disk. Use Python's `RotatingFileHandler` to automatically archive old logs:
```python
from logging.handlers import RotatingFileHandler
handler = RotatingFileHandler('app.log', maxBytes=10*1024*1024, backupCount=5)
# Max 10MB per file, keep last 5 files
```
[/CALLOUT]

---

## The Deployment Checklist

Before you deploy anything to production:

```
  Security:
  [ ] Never hardcode passwords or API keys in code
  [ ] Set DEBUG=False in production
  [ ] Use HTTPS (SSL certificate)

  Performance:
  [ ] Test with realistic load (not just 1 user)
  [ ] Set up database indexes on frequently searched columns
  [ ] Enable caching for slow, repeated queries

  Reliability:
  [ ] Set up logging and monitoring
  [ ] Configure log rotation
  [ ] Set up alerts for when the app crashes

  Process:
  [ ] All tests pass
  [ ] Code has been reviewed by another person
  [ ] You can ROLL BACK (undo) if something goes wrong
```

---

## Glossary

| Term | Meaning |
|:---|:---|
| **Deployment** | Making your app available to real users on the internet |
| **IaaS** | Infrastructure as a Service — renting raw servers |
| **PaaS** | Platform as a Service — renting a platform with tools pre-installed |
| **SaaS** | Software as a Service — using a complete ready-made software product |
| **CI** | Continuous Integration — automatically testing code on every push |
| **CD** | Continuous Deployment — automatically deploying code if tests pass |
| **Docker** | A tool that packages your app + environment into a portable container |
| **Container** | An isolated package with an app and everything it needs to run |
| **Logging** | Recording events and errors from your app into a file |
| **Log Rotation** | Archiving old log files so they don't fill the disk |
