# Authentication with Flask-Login Object

**Flask-Login** is the standard extension for managing user sessions. It handles the "heavy lifting" of authentication, such as logging users in, logging them out, and remembering their sessions over extended periods.

## Key Components

### 1. UserMixin
Your `User` class should inherit from `UserMixin`. This provides default implementations for methods that Flask-Login expects:
- `is_authenticated`
- `is_active`
- `is_anonymous`
- `get_id()`

### 2. LoginManager
The central object that manages authentication. You link it to your app using `login_manager.init_app(app)`.

### 3. User Loader
A mandatory callback function that tells Flask-Login how to reload the user object from the user ID stored in the session.
```python
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

## Recommended Project Structure
When using extensions, the structure remains consistent but cleaner:

```text
my_flask_app/
├── app.py              # Main logic with Flask-Login setup
└── templates/
    ├── login.html      
    └── dashboard.html  
```

---

## Comparison: Session vs. Flask-Login

| Feature | Built-in Session (Manual) | Flask-Login (Extension) |
| :--- | :--- | :--- |
| **Effort** | Low setup, high manual code. | Moderate setup, automated code. |
| **Logic** | You write `if 'user' in session` manually. | Just use the `@login_required` decorator. |
| **User Object** | You only have a string/ID in session. | You get a full `current_user` object everywhere. |
| **Reliability** | Prone to human error (forgetting checks). | Standardized, robust, and industry-standard. |

[TIP]
**Conclusion**: Use the manual session method for extremely simple prototypes. For any application meant for users, **Flask-Login** is the safer and more professional choice.
[/CALLOUT]
