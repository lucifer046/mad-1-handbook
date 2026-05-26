# Flask Session Management Example

from flask import Flask, session, redirect, url_for, request

app = Flask(__name__)

# Secret key is required to sign the session cookie
# In production, use a long, random string
app.secret_key = 'super-secret-key-that-should-be-kept-safe'

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]} | <a href="/logout">Logout</a>'
    return 'You are not logged in | <a href="/login">Login</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Authentication logic (check db, etc.)
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # Remove the username from the session
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
