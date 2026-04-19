from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
app.secret_key = 'sac_mad_one_flask_login_week'

# 1. Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'sign_in' # Where to redirect unauthorized users

# 2. User Model (Inherits UserMixin for auth properties)
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# 3. Mock Database
users = {'admin': User('admin')}

# 4. User Loader: Reloads the user object from the session ID
@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form.get('username')
        # Hardcoded password check
        if username in users and request.form.get('pwd') == '123':
            login_user(users[username]) # Standard method to start a session
            return redirect(url_for('dashboard'))
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/dashboard')
@login_required # Automatically checks if user is logged in
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def sign_out():
    logout_user() # Standard method to clear the login session
    return "Logged out successfully"

if __name__ == '__main__':
    app.run(debug=True)
