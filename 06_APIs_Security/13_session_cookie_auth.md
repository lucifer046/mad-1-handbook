# Session-Based Authentication (The Cookie Method)

The simplest way to handle user state in Flask is using the built-in `session` object. This method relies on **Signed Cookies** to store data on the client side.

## Core Concepts

### 1. The Secret Key
Flask uses a `secret_key` to cryptographically sign the session cookie. This prevents users from tampering with the cookie data.
```python
app.secret_key = 'your_super_secret_key'
```

### 2. The Session Object
The `session` object acts like a dictionary that persists across requests.
- **Set Data**: `session['user'] = username`
- **Check Data**: `if 'user' in session:`
- **Clear Data**: `session.clear()` (Ideal for logout).

## Recommended Project Structure
For a standard Flask application, organize your files as follows:

```text
my_flask_app/
├── app.py              # Main logic (contains the code shown here)
└── templates/          # HTML files
    ├── login.html      # Login form
    └── dashboard.html  # Protected page
```

---

## The Workflow
1.  **Login**: User submits credentials -> Server verifies -> Server sets `session['user']`.
2.  **Protected Access**: User requests `/dashboard` -> Server checks `if 'user' in session` -> If yes, render page; if no, show error.
3.  **Logout**: User requests `/logout` -> Server calls `session.clear()` -> User is "forgotten".

[WARNING]
**Security Limitation**: With this manual method, you must remember to add the check (`'user' in session`) to **every single protected route**. Forgetting it even once creates a security hole.
[/CALLOUT]
