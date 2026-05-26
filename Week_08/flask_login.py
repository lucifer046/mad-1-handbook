from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
app.secret_key = 'sac_mad_one_flask_login_week'

# 1. Configure LoginManager
# Why? This object handles the complex logic of tracking sessions,
# handling redirects for unauthorized users, and loading user objects.
login_manager = LoginManager()
login_manager.init_app(app)

# 2. Set the Login View
# Why? If a user tries to access a @login_required route, 
# Flask-Login needs to know which page to send them to for signing in.
login_manager.login_view = 'sign_in' 

# 3. User Model with UserMixin
# Why UserMixin? It provides standard attributes like 'is_authenticated'.
# Without this, you'd have to manually define 4-5 properties for every User class.
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Mock Database
users = {'admin': User('admin')}

# 4. The User Loader (CRITICAL)
# Why? Flask-Login only stores the User ID in the cookie.
# This function is called on EVERY request to convert that ID back into a real User object.
@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form.get('username')
        # 5. login_user() function
        # Why? This is the standardized way to start a session in Flask-Login.
        # It handles the cookie creation and links it to the User Loader.
        if username in users and request.form.get('pwd') == '123':
            login_user(users[username])
            return redirect(url_for('dashboard'))
            
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/dashboard')
# 6. The @login_required Decorator
# Why? This is the killer feature. Instead of manual 'if' checks, 
# this decorator handles the authorization automatically.
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def sign_out():
    # 7. logout_user()
    # Why? It properly cleans up the Flask-Login session and cookie.
    logout_user()
    return "Logged out successfully"

if __name__ == '__main__':
    app.run(debug=True)
