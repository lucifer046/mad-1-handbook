# RESTful API Implementation in Flask

from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock Database
students = [
    {"id": 101, "name": "Alice", "hostel": "Godavari"},
    {"id": 102, "name": "Bob", "hostel": "Cauvery"}
]

@app.route('/api/students', methods=['GET'])
def get_students():
    """Retrieve all students (Read)."""
    return jsonify(students)

@app.route('/api/students', methods=['POST'])
def create_student():
    """Create a new student (Create)."""
    new_student = request.json
    students.append(new_student)
    return jsonify(new_student), 201

@app.route('/api/students/<int:sid>', methods=['PUT'])
def update_student(sid):
    """Update an existing student (Update)."""
    student = next((s for s in students if s['id'] == sid), None)
    if student:
        student.update(request.json)
        return jsonify(student)
    return jsonify({"error": "Not found"}), 404

@app.route('/api/students/<int:sid>', methods=['DELETE'])
def delete_student(sid):
    """Remove a student (Delete)."""
    global students
    students = [s for s in students if s['id'] != sid]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
