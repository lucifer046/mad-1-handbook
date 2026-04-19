from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'sac_mad_one_flask_login_week' # Required for session encryption

@app.route('/login', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Hardcoded verification (In production, use hashed database checks)
        if username == 'admin' and password == '12345':
            session['user'] = username
            return redirect(url_for('dashboard'))
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Manual Session Check
    if 'user' in session:
        return render_template('dashboard.html')
    return "Unauthorized access - please login"

@app.route('/logout')
def sign_out():
    session.clear() # Deletes all session information, effectively logging out
    return "Logged out successfully"

if __name__ == '__main__':
    app.run(debug=True)
