# Example of a simple MVC-style structure in Python
# This demonstrates the 'Student Gradebook' running example

class StudentModel:
    """The Model: Manages student data."""
    def __init__(self):
        self.students = {} # {id: name}
        
    def add_student(self, student_id, name):
        self.students[student_id] = name
        
    def get_all_students(self):
        return self.students

class GradeView:
    """The View: Handles how data is displayed."""
    @staticmethod
    def render_list(student_dict):
        print("--- STUDENT LIST ---")
        for sid, name in student_dict.items():
            print(f"ID: {sid} | Name: {name}")
        print("--------------------")

class GradeController:
    """The Controller: Connects Model and View."""
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
    def handle_add_student(self, sid, name):
        # Business logic: validate input
        if not sid or not name:
            return "Error: Invalid input"
        self.model.add_student(sid, name)
        
    def update_display(self):
        data = self.model.get_all_students()
        self.view.render_list(data)

# Usage
if __name__ == "__main__":
    m = StudentModel()
    v = GradeView()
    c = GradeController(m, v)
    
    c.handle_add_student("S101", "Alice Smith")
    c.handle_add_student("S102", "Bob Jones")
    c.update_display()
