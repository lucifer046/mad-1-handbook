# Basic Flask Application Example

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mock database
students = [
    {"id": 101, "name": "Alice"},
    {"id": 102, "name": "Bob"}
]

@app.route('/')
def home():
    """Renders the homepage with student list."""
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    """Handles adding a new student."""
    if request.method == 'POST':
        name = request.form.get('name')
        new_id = students[-1]['id'] + 1 if students else 101
        students.append({"id": new_id, "name": name})
        return redirect(url_for('home'))
    
    return '''
        <form method="post">
            Name: <input type="text" name="name">
            <input type="submit" value="Add">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True, port=5000)
