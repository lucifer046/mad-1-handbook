# API Design, REST & Flask-RESTful

## 1. What is an API?

An **API (Application Programming Interface)** is a defined interface that allows two different programs to communicate with each other. It acts as a middleman or "waiter" that abstracts the internal implementation details of a system, serving only structured endpoints.

```
  YOUR APP (Frontend)            WEATHER API (Backend)           WEATHER DATABASE
           │                              │                              │
           │ "GET /weather?city=Mumbai"   │                              │
           ├─────────────────────────────>│                              │
           │                              │ "SELECT * FROM weather..."   │
           │                              ├─────────────────────────────>│
           │                              │            data              │
           │                              │<─────────────────────────────┤
           │  { "temp": 32, "rain": 0 }   │                              │
           │<─────────────────────────────┤                              │
           ▼                              ▼                              ▼
```

---

## 2. REST: Architectural Principles

To make APIs predictable and standard, developers follow **REST** (Representational State Transfer) guidelines.

### The 6 REST Constraints
1.  **Client-Server Separation**: The user interface (client) and the database storage (server) are separate. They only interact via HTTP requests.
2.  **Statelessness**: Every request must contain all the information necessary to understand and process it. The server does not store session context.
3.  **Cacheability**: Responses must declare themselves as cacheable or non-cacheable to optimize network traffic.
4.  **Uniform Interface**: Resources use consistent naming conventions and standard HTTP methods. No verbs in URLs (e.g., `/api/students`, not `/getStudents`).
5.  **Layered System**: The client cannot tell if it is connected directly to the end server or through an intermediary (like a CDN, proxy, or load balancer).
6.  **Code on Demand (Optional)**: Servers can temporarily extend client functionality by transferring executable code (e.g., JavaScript).

### Resources and standard URL Naming Conventions
In REST, all entities are treated as **resources** and represented using plural nouns:

*   `GET /api/students` → Retrieve a collection of all students.
*   `POST /api/students` → Create a new student record.
*   `GET /api/students/101` → Retrieve one specific student (ID = 101).
*   `PUT /api/students/101` → Replace/update student 101 completely.
*   `DELETE /api/students/101` → Remove student 101 from the system.

---

## 3. HTTP Methods & Idempotency

**Idempotency** means that making multiple identical requests has the same side-effect as making a single request.

| HTTP Method | CRUD | Idempotent? | Explanation |
| :--- | :--- | :--- | :--- |
| **GET** | Read | **YES** | Reading the same resource 100 times does not modify database state |
| **PUT** | Update / Create | **YES** | Replacing a field to "Alice" repeatedly leaves the state as "Alice" |
| **DELETE** | Delete | **YES** | Deleting a record once or 10 times results in it being absent |
| **POST** | Create | **NO** | Sending a POST 5 times will create 5 duplicate resources |
| **PATCH** | Partial Update | **NO** | Incrementing or modifying a field relative to its current state varies |

---

## 4. HTTP Status Codes

| Category | Range | Meaning | Examples |
| :--- | :--- | :--- | :--- |
| **Informational** | `1xx` | Request received, continuing process | `100 Continue` |
| **Success** | `2xx` | Action successfully received and accepted | `200 OK`, `201 Created` |
| **Redirection** | `3xx` | Further action needed to complete request | `301 Moved Permanently` |
| **Client Error** | `4xx` | Request contains bad syntax or cannot be fulfilled | `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found` |
| **Server Error** | `5xx` | Server failed to fulfill an apparently valid request | `500 Internal Server Error` |

---

## 5. Flask Routes (`@app.route`) vs. Flask-RESTful (`Resource`)

Flask-RESTful is an extension that encourages clean class-based views called **Resources**, which automatically map methods (`get`, `post`, `put`, `delete`) to standard HTTP verbs.

| Feature | Standard Flask Routes | Flask-RESTful Resources |
| :--- | :--- | :--- |
| **Setup** | Uses `@app.route()` decorator | Inherits from `Resource` class, registered via `api.add_resource` |
| **HTTP Actions** | Conditional `if request.method == 'POST'` blocks | Native class methods `def get(self):`, `def post(self):` |
| **Serialization** | Requires explicit `jsonify(data)` | Returns Python dictionaries directly, automatically serialized |
| **Input Parsing** | Manually parses `request.json` | Uses declarative parser `reqparse.RequestParser` |

### Code Comparison

#### Using standard `@app.route`
```python
from flask import Flask, jsonify, request

app = Flask(__name__)
users = {"1": {"name": "Alice"}}

@app.route('/user/<string:user_id>', methods=['GET', 'POST'])
def handle_user(user_id):
    if request.method == 'GET':
        return jsonify(users.get(user_id, "Not Found"))
    elif request.method == 'POST':
        users[user_id] = request.json
        return jsonify({"message": "User added", "data": users[user_id]}), 201
```

#### Using Flask-RESTful Class-based Resource
```python
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
users = {"1": {"name": "Alice"}}

class UserResource(Resource):
    def get(self, user_id):
        return users.get(str(user_id), {"error": "Not Found"}), 200

    def post(self, user_id):
        users[str(user_id)] = request.json
        return {"message": "User added", "data": users[str(user_id)]}, 201

api.add_resource(UserResource, '/user/<int:user_id>')
```

---

## 6. Complete CRUD Database Integration (Flask-RESTful + SQLAlchemy)

Here is a full integration architecture using SQLite and Flask-SQLAlchemy models.

```python
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

# Database Model
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Bootstrap Database Tables
with app.app_context():
    db.create_all()

# Setup Request Parser
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help="Name is required")
parser.add_argument('email', type=str, required=True, help="Email is required")

# Resource Controller
class UserAPI(Resource):
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if user:
            return {"id": user.id, "name": user.name, "email": user.email}, 200
        return {"message": "User not found"}, 404

    def post(self, user_id):
        if UserModel.query.get(user_id):
            return {"message": "User already exists"}, 400
        
        args = parser.parse_args()
        new_user = UserModel(id=user_id, name=args['name'], email=args['email'])
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User added", "id": new_user.id}, 201

    def put(self, user_id):
        user = UserModel.query.get(user_id)
        args = parser.parse_args()
        
        if not user:
            # IDEMPOTENCY: Create resource if it does not exist
            user = UserModel(id=user_id, name=args['name'], email=args['email'])
            db.session.add(user)
        else:
            # Update fields
            user.name = args['name']
            user.email = args['email']
            
        db.session.commit()
        return {"message": "User updated", "id": user.id}, 200

    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted"}, 200
        # IDEMPOTENCY: If user is already deleted, response remains successful (200 OK)
        return {"message": "User not found (already absent)"}, 200

# Map Endpoint Route
api.add_resource(UserAPI, '/api/user/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 7. Data Serialization (Python vs. JavaScript)

Serialization is the process of converting a language-specific object (like a Python dictionary) into a string structure (like JSON) that can be sent over a network.

### Python JSON Utilities
*   **`json.dumps(obj)`**: Converts a Python dictionary/list to a JSON **string**.
*   **`json.dump(obj, file_handler)`**: Serializes and writes a Python object directly to an open **file**.
*   **`flask.jsonify(*args, **kwargs)`**: Converts Python objects to a Flask `Response` object and automatically injects the HTTP header `Content-Type: application/json`.

```python
import json

data = {"name": "Alice", "age": 30}

# json.dumps -> returns string
string_data = json.dumps(data) 

# json.dump -> writes to a file
with open("data.json", "w") as f:
    json.dump(data, f)
```

### JavaScript JSON Utilities
*   **`JSON.stringify(obj)`**: Converts a JavaScript object/array to a JSON **string**.
*   **`JSON.parse(string)`**: Parses a JSON string to construct a JavaScript value/object.

```javascript
const obj = { name: "Alice", age: 30 };
const jsonStr = JSON.stringify(obj); // Returns string
const parsedObj = JSON.parse(jsonStr); // Returns JavaScript Object
```

### Fetch API Example (Client-Side API Consuming)
```javascript
// Fetch user profile from the Flask endpoint
fetch('http://127.0.0.1:5000/api/user/1')
  .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not OK');
      }
      return response.json(); // Deserialize response to JS Object
  })
  .then(data => console.log(data))
  .catch(err => console.error('Fetch Error:', err));
```

---

## 8. Response Field Formatting: `marshal` and `marshal_with`

In Flask-RESTful, we can control and filter response properties (hiding sensitive fields like passwords) using field declarations.

### `marshal` (Manual Function)
Used to format single dictionaries or lists manually:
```python
from flask_restful import marshal, fields

resource_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String
}

data = {
    'id': 101,
    'username': 'alice1',
    'email': 'alice@example.com',
    'password_hash': 'pbkdf2:sha256:260000$secret' # Hidden from output
}

formatted_response = marshal(data, resource_fields)
print(formatted_response)
# Output: {'id': 101, 'username': 'alice1', 'email': 'alice@example.com'}
```

### `@marshal_with` (Automatic Decorator)
Applied as a decorator directly above Resource method definitions:
```python
from flask_restful import Resource, fields, marshal_with

user_fields = {
    'id': fields.Integer,
    'username': fields.String
}

class UserProfile(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        # We can return an object or raw database dict
        # marshal_with will filter out extra fields automatically!
        return {
            'id': user_id,
            'username': 'alice1',
            'email': 'alice@example.com',
            'session_token': 'secret-token'
        }
```

---

## Glossary

| Term | Meaning |
| :--- | :--- |
| **API** | Application Programming Interface. standard boundary interface for program integrations |
| **REST** | Architectural style leveraging HTTP constraints and standards for server operations |
| **Statelessness** | Server architectural constraint where every client request contains complete parameters |
| **Resource** | Any primary database entity exposed through API endpoints |
| **Idempotency** | Safety guarantee where multiple requests cause zero added side-effects |
| **Serialization** | Process converting program storage structures into network transmission formats (JSON) |
| **Marshal** | Restructuring raw database dicts/objects to strict schema definitions |
