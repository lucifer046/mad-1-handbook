# Testing with Pytest

## Why Do We Test?

Imagine you built a student portal. It works fine on your laptop. You deploy it. A student types in 100 marks and the app crashes because you forgot to handle numbers above 99.

**Testing** is how we catch these bugs *before* users do. It's also how we make sure that when we fix one bug, we don't accidentally break three others.

---

## Types of Testing: Static vs. Dynamic

Before we dive into tools like Pytest, we must understand *how* we approach testing. Testing isn't just about running scripts; it’s about verifying correctness at different stages.

### 1. Static Testing (Testing the "Paper")
Static testing is performed **without executing the code**. It involves checking the code, documentation, and design to find errors.

*   **Examples:** Code reviews, walkthroughs, inspections, and using "Linters" (like Flake8) to catch syntax errors.
*   **Pros:** 
    *   **Early Detection:** Catches bugs before they ever reach a computer.
    *   **Cost-Effective:** Fixing a design flaw on paper is 10x cheaper than fixing it in production.
    *   **Quality Culture:** Encourages developers to write cleaner code.
*   **Cons:** 
    *   Cannot detect runtime errors (e.g., "Division by zero" which only happens during execution).
    *   Cannot verify performance or user experience.

### 2. Dynamic Testing (Testing the "Action")
Dynamic testing is performed **by executing the code**. You provide inputs and verify if the outputs match expectations.

*   **Examples:** Unit tests (Pytest), Integration tests, and User Acceptance Testing (UAT).
*   **Pros:** 
    *   **Runtime Validation:** Catches memory leaks, logic errors, and performance bottlenecks.
    *   **Functional Accuracy:** Ensures the app actually *works* for the user.
*   **Cons:** 
    *   More expensive to set up (requires a test environment).
    *   May miss bugs if the specific logic path isn't triggered by an input.

---

## Testing Methodologies: The "Box" Approach

How much should the tester know about the code? This determines the "color" of the box.

| Methodology | Definition | Pros | Cons |
|:--- |:--- |:--- |:--- |
| **Black Box** | Testing from the **user's perspective**. The tester has zero knowledge of the internal code. | User-centric; Tester doesn't need to be a developer. | Can lead to redundant tests; impossible to test every logic path. |
| **White Box** | Testing from the **developer's perspective**. The tester has full access to the source code and logic. | High code coverage; identifies hidden bugs in loops/logic. | Requires high technical skill; very time-consuming. |
| **Grey Box** | A **hybrid approach**. The tester has partial knowledge (e.g., knows the database schema or API endpoints but not the code). | Finds integration issues easily; combined benefits of both. | Coverage is limited compared to pure white box testing. |

---

## What is Pytest?

**Pytest** is a Python module (testing framework) used to write and run automated tests. It is the most popular testing tool in Python because of three key advantages:

```
   Pytest Advantages:

   1. Auto-Discovery  → Automatically finds and runs test files,
                        classes, and functions — no configuration
                        needed.

   2. Simple Syntax   → Uses plain Python assert statements.
                        No special syntax to learn.

   3. Parametrize     → Run the same test with many sets of input
                        data using a single decorator.
```

Install it with:
```bash
pip install pytest
```

---

## The Golden Rules: Naming Conventions

Pytest's auto-discovery relies entirely on naming. If you don't follow these rules, Pytest won't find your tests.

```
   Rule 1: FILES must start with "test_" or end with "_test"
           Good:  test_marks.py   marks_test.py
           Bad:   marks.py        check_marks.py

   Rule 2: FUNCTIONS must start with "test_"
           Good:  def test_case1():
           Bad:   def case1():    def check_case():

   Rule 3: CLASSES must start with "Test"
           Good:  class TestMarks:
           Bad:   class Marks:    class marks_test:
```

---

## The `assert` Keyword

The `assert` keyword is the fundamental building block of every test. It checks if a condition is `True`. If it's `False`, Python raises an `AssertionError` and the test fails.

```python
# assert <condition>, "Optional error message"

assert 2 + 2 == 4          # PASSES silently
assert 2 + 2 == 5          # FAILS with AssertionError
assert "hello" in "hello world"  # PASSES
assert [] == []             # PASSES
```

[NOTE]
`assert` is just a Python keyword — it's not special to Pytest. But Pytest intercepts the `AssertionError` and produces a clean, readable failure report with the actual vs. expected values.
[/CALLOUT]

---

## Running Pytest: CLI Commands

```bash
# Run all tests in the current directory (auto-discovery)
pytest

# Run with verbose mode — see each test name and PASSED/FAILED
pytest -v

# Run only tests whose name contains a keyword
pytest -k "increment"

# Run tests in a specific file
pytest test_compute.py

# Run a specific function in a specific file
pytest test_compute.py::test_increment
```

### How `pytest -k` Works
The `-k` flag filters tests by a keyword match against their name.
```bash
# Run only tests whose name contains "increment"
pytest -k "increment"

# Run tests whose name contains "increment" OR "decrement"
pytest -k "increment or decrement"

# Run all tests EXCEPT those containing "slow"
pytest -k "not slow"
```

---

## Part 1: Testing Logic (Functions)

### The Application Code
This is a simple `compute` function we want to test — it either increments or decrements a value.

```python
# compute.py  (the code we are testing)

def compute(value, action):
    """
    Performs an arithmetic operation on a value.

    Args:
        value (int): The starting number.
        action (str): Either 'increment' or 'decrement'.

    Returns:
        int: The result of the operation.

    Raises:
        ValueError: If an unknown action is provided.
    """
    if action == "increment":
        return value + 1
    elif action == "decrement":
        return value - 1
    else:
        raise ValueError(f"Unknown action: {action}")
```

### The Test File

```python
# test_compute.py  (the test file — note the "test_" prefix)

import pytest
from compute import compute

# --- Basic Tests ---

def test_increment():
    """Verify that increment adds 1 to the value."""
    result = compute(5, "increment")
    assert result == 6

def test_decrement():
    """Verify that decrement subtracts 1 from the value."""
    result = compute(10, "decrement")
    assert result == 9

def test_increment_from_zero():
    """Edge case: incrementing zero should give 1."""
    assert compute(0, "increment") == 1

def test_invalid_action_raises_error():
    """An unknown action should raise a ValueError."""
    with pytest.raises(ValueError):
        compute(5, "multiply")  # Should throw ValueError
```

Run with `pytest -v` and you'll see:
```
test_compute.py::test_increment              PASSED
test_compute.py::test_decrement              PASSED
test_compute.py::test_increment_from_zero   PASSED
test_compute.py::test_invalid_action_raises_error PASSED
```

---

## Part 2: Advanced Pytest Features

### 1. Pytest Markers
**Markers** are decorators (`@pytest.mark.<name>`) that attach metadata or special behavior to a test function.

#### Built-in Marker 1: `@pytest.mark.skip`
Skips a test unconditionally. Use this when a feature is not yet implemented.
```python
@pytest.mark.skip(reason="Feature not yet implemented")
def test_multiply():
    result = compute(5, "multiply")
    assert result == 25
```

#### Built-in Marker 2: `@pytest.mark.skipif`
Skips a test only if a condition is met. Great for OS-specific or environment-specific tests.
```python
import sys

@pytest.mark.skipif(sys.platform == "win32", reason="Does not run on Windows")
def test_linux_only_feature():
    # This test will be SKIPPED on Windows, but RUN on Linux/Mac
    assert True
```

#### Built-in Marker 3: `@pytest.mark.parametrize`
Runs the **same test function** multiple times with different input data. This replaces writing 5 separate test functions for 5 cases.
```python
@pytest.mark.parametrize("value, action, expected", [
    (5,  "increment", 6),   # case 1
    (10, "increment", 11),  # case 2
    (10, "decrement", 9),   # case 3
    (0,  "decrement", -1),  # case 4 — edge case
    (99, "increment", 100), # case 5
])
def test_compute_parametrized(value, action, expected):
    assert compute(value, action) == expected
```

#### Built-in Marker 4: `@pytest.mark.xfail`
Expects the test to fail. If it fails, the test suite still passes. Great for documenting active bugs.
```python
@pytest.mark.xfail(reason="Bug #101")
def test_feature():
    assert 1 == 2
```

#### Custom (User-Defined) Markers
You can group tests into custom tags by declaring them.
```python
# Register custom markers in pytest.ini:
# [pytest]
# markers =
#     smoke: Critical path tests
#     slow: Long running tests

@pytest.mark.smoke
def test_app_starts():
    assert compute(1, "increment") == 2
```
Run only smoke tests: `pytest -m smoke`

---

### 2. Pytest Fixtures
Fixtures are functions that run before (and sometimes after) tests. They are perfect for setting up test context, databases, or client states.

[NOTE]
**Analogy:** Think of a fixture like a butler who sets your table before every meal (test) and cleans it up after you're done.
[/CALLOUT]

```python
import pytest

@pytest.fixture
def sample_list():
    return [1, 2, 3]

def test_sum(sample_list):
    assert sum(sample_list) == 6
```

#### Scopes of a Fixture
The `scope` parameter controls how often the fixture is executed:
*   `function` (default): Setup and teardown runs fresh for **every single test function**.
*   `class`: Runs once per test class.
*   `module`: Runs once per test file (module).
*   `session`: Runs once for the entire test run session (e.g., starting a database container).

```python
@pytest.fixture(scope="module")
def connect_db():
    print("\nConnecting to Database once...")
    yield "database_session"
    print("\nDisconnecting from Database...")
```

---

### 3. Shared Fixtures with `conftest.py`
If you need to share fixtures across multiple files, Pytest looks for a special file named `conftest.py`. You do not need to import fixtures from `conftest.py` — Pytest handles it automatically.

[NOTE]
**Analogy:** Like putting shared spoons in a central kitchen drawer (`conftest.py`) instead of keeping separate duplicate drawers at every single dining table.
[/CALLOUT]

```
project/
├── tests/
│   ├── test_math.py
│   ├── test_string.py
│   └── conftest.py
```

#### conftest.py
```python
import pytest

@pytest.fixture
def fruit_basket():
    return ["apple", "banana", "cherry"]
```

#### test_math.py
```python
def test_banana_in_basket(fruit_basket):
    assert "banana" in fruit_basket
```

---

## Part 3: Testing Flask Web Applications

In modern web development, we test Flask applications using two distinct methods depending on the scope of testing.

### Method A: Live API Requests (Integration & System Testing)
This method sends real HTTP requests to a running Flask server. It treats the application as a **Black/Grey box**.

#### The Flask Application (`app.py`)
```python
from flask import Flask, request, jsonify

app = Flask(__name__)
students = []

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students), 200

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    students.append(data)
    return jsonify({"message": "Student added", "student": data}), 201
```

#### The API Test File (`test_api.py`)
```python
import requests
import pytest

BASE_URL = "http://127.0.0.1:5000"

# Note: Start the Flask app ('python app.py') manually before running.
def test_get_students_status_200():
    response = requests.get(f"{BASE_URL}/students")
    assert response.status_code == 200

def test_post_student():
    new_student = {"name": "Alice", "marks": 85}
    response = requests.post(f"{BASE_URL}/students", json=new_student)
    assert response.status_code == 201
    assert response.json()["student"]["name"] == "Alice"
```

---

### Method B: Idiomatic Client Mocking (Unit & Integration Testing)
This method does **not** require starting a local server. We use a Pytest fixture to inject Flask's built-in `test_client()`. It represents a **White/Grey box** approach.

#### The Test File (`test_app.py`)
```python
import pytest
from app import app  # Import your Flask app instance

@pytest.fixture
def client():
    # 1. Enable testing configurations
    app.config['TESTING'] = True
    
    # 2. Yield Flask's test client
    with app.test_client() as client:
        yield client  # Testing happens here
        
    # 3. Clean up actions (if database operations are involved)

def test_index_route(client):
    """GET / should return 200 OK and Hello message."""
    response = client.get('/')
    assert response.status_code == 200
    
    # response.data returns a byte-string, so we use 'b' prefix
    assert b'Hello, World!' in response.data

def test_about_route(client):
    """GET /about should return about description."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'This is the about page' in response.data

def test_greet_route(client):
    """GET /greet/<name> should greet dynamically."""
    response = client.get('/greet/Alice')
    assert response.status_code == 200
    assert b'Hello, Alice!' in response.data
```

[TIP]
**Key Takeaways for Flask test_client()**:
1. **No active server needed**: Runs natively in Pytest's process context.
2. **Byte strings comparison**: `response.data` returns raw bytes. Always compare with byte literals using the `b` prefix (e.g. `b'Hello'`) or decode it with `response.data.decode('utf-8')`.
3. **Methods simulation**: Simulates requests using `client.get()`, `client.post()`, `client.put()`, etc.
[/CALLOUT]

---

## The Testing Pyramid

```
                                        /\
                                       /  \
                                      /    \
                                     /  UA  \
                                    /  TEST  \
                                   / (Accept) \
                                  /────────────\
                                 /  INTEGRATION \
                                /     TESTS      \
                               / (Routes & DB)    \
                              /────────────────────\
                             /      UNIT TESTS      \
                            /  (Fast, Many, Auto)    \
                           /   Pure logic/functions   \
                          /____________________________\
```

---

## Bonus Reference Table: Testing Types & Focus Areas

| **Test Type** | **Focus Area** | **Box Strategy** |
| :--- | :--- | :--- |
| **Unit Testing** | Smallest isolated blocks (functions, methods, helpers). | White Box |
| **Integration Testing** | Dynamic communication between routes, ORM database, and view layers. | Grey Box |
| **System Testing** | Full application performance, deployment structures, and routing flows. | Black / Grey Box |
| **User Acceptance Testing (UAT)**| Verification of features against requirements by actual clients. | Black Box |

---

## Glossary

| Term | Meaning |
|:---|:---|
| **pytest** | Python testing framework with auto-discovery and clean syntax |
| **assert** | Python keyword that checks a condition — fails with `AssertionError` if `False` |
| **Marker** | A decorator (`@pytest.mark.*`) that adds metadata or behavior to a test |
| **@pytest.mark.skip** | Unconditionally skips a test |
| **@pytest.mark.skipif** | Skips a test only if a condition is `True` |
| **@pytest.mark.parametrize** | Runs one test function with multiple sets of inputs |
| **@pytest.mark.xfail** | Expects a test to fail (ideal for active/open bug tracking) |
| **conftest.py** | Central drawer containing shared fixtures automatically loaded by Pytest |
| **Fixture** | Setup and teardown functions providing reusable contexts/mocks to tests |
| **`yield`** | Keyword in fixtures separating pre-test setup from post-test teardown |
| **`test_client()`** | Flask method returning a virtual browser context for API testing without live servers |
| **Byte String (`b'..'`)**| Sequence of raw bytes. Required when asserting on Flask's raw `response.data` |
| **Static Testing** | Testing code/docs without execution (Reviews, Linting) |
| **Dynamic Testing** | Testing by executing code (Unit tests, Integration) |
| **Black Box** | Testing from a user perspective with zero code knowledge |
| **White Box** | Testing from a developer perspective with full code access |
| **Grey Box** | Hybrid testing with partial knowledge of internals |
