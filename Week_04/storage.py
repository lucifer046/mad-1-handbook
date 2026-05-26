# Persistent Storage Example: Student Class and CSV

import csv
import os

class Student:
    """A class representing a student with a persistent ID."""
    id_next = 1 # Class variable for auto-increment

    def __init__(self, name, hostel_id):
        self.id = Student.id_next
        Student.id_next += 1
        self.name = name
        self.hostel_id = hostel_id

    def to_dict(self):
        return {"id": self.id, "name": self.name, "hostel_id": self.hostel_id}

# Demonstrating CSV Persistence
def save_students(students, filename="students.csv"):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "hostel_id"])
        writer.writeheader()
        for s in students:
            writer.writerow(s.to_dict())
    print(f"Saved {len(students)} students to {filename}")

def load_students(filename="students.csv"):
    if not os.path.exists(filename): return []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)

# Usage
if __name__ == "__main__":
    s1 = Student("Alice", "H1")
    s2 = Student("Bob", "H2")
    
    save_students([s1, s2])
    
    loaded = load_students()
    print("Loaded data:", loaded)
