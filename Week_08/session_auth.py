from flask import Flask, render_template, request, session, redirect, url_for

# 1. Initialize the Flask application
app = Flask(__name__)

# 2. Set the Secret Key (CRITICAL)
# Flask uses this to cryptographically sign session cookies. 
# Without this, session data can be easily tampered with by the user.
app.secret_key = 'sac_mad_one_flask_login_week' 

@app.route('/login', methods=['GET', 'POST'])
def sign_in():
    # 3. Check if the user is submitting the login form
    if request.method == 'POST':
        # Retrieve form data
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 4. Verification Logic
        # Why hardcoded? For educational purposes to show the session mechanism.
        # In a real app, you would query a database and check hashed passwords.
        if username == 'admin' and password == '12345':
            # 5. Create a Session
            # We store the username in the 'session' dictionary. 
            # This triggers Flask to send a 'Set-Cookie' header to the browser.
            session['user'] = username
            return redirect(url_for('dashboard'))
            
        return "Invalid credentials"
        
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # 6. Manual Authorization Check
    # Why? Flask sessions don't automatically protect routes.
    # We must manually check if the key exists in the session for EVERY protected page.
    if 'user' in session:
        return render_template('dashboard.html')
        
    # If not in session, block access
    return "Unauthorized access - please login"

@app.route('/logout')
def sign_out():
    # 7. Clear the Session
    # session.clear() removes all keys from the session dictionary.
    # The browser still has the cookie, but the server no longer recognizes it.
    session.clear() 
    return "Logged out successfully"

if __name__ == '__main__':
    app.run(debug=True)
