# ============================================================
# PYTEST COMPLETE SUMMARY — MAD-I Handbook
# ============================================================
# Topics covered:
#   1. Naming Conventions (auto-discovery)
#   2. assert keyword
#   3. pytest -v and pytest -k
#   4. Testing logic functions (compute)
#   5. Markers: skip, skipif, parametrize
#   6. Custom markers (smoke, regression, slow)
#   7. Testing Flask API routes with requests
# ============================================================

import sys
import pytest
import requests


# ------------------------------------------------------------
# SECTION 1: The Code Under Test (compute function)
# In a real project, this would live in compute.py
# ------------------------------------------------------------

def compute(value, action):
    """
    Perform an arithmetic operation.

    Args:
        value (int): Starting number.
        action (str): 'increment' or 'decrement'.

    Returns:
        int: Result after applying the action.

    Raises:
        ValueError: If action is neither 'increment' nor 'decrement'.
    """
    if action == "increment":
        return value + 1
    elif action == "decrement":
        return value - 1
    else:
        raise ValueError(f"Unknown action: '{action}'")


# ============================================================
# SECTION 2: Basic Test Cases
# File must be named test_*.py for Pytest auto-discovery.
# Functions must start with test_
# ============================================================

def test_increment():
    """increment should add 1 to the value."""
    assert compute(5, "increment") == 6

def test_decrement():
    """decrement should subtract 1 from the value."""
    assert compute(10, "decrement") == 9

def test_increment_from_zero():
    """Edge case: 0 + 1 = 1."""
    assert compute(0, "increment") == 1

def test_decrement_to_negative():
    """Edge case: 0 - 1 = -1."""
    assert compute(0, "decrement") == -1

def test_invalid_action_raises_error():
    """An unknown action string must raise a ValueError."""
    with pytest.raises(ValueError):
        compute(5, "multiply")   # Should crash with ValueError


# ============================================================
# SECTION 3: Markers — @pytest.mark.skip
# Use when a feature is not yet implemented.
# ============================================================

@pytest.mark.skip(reason="multiply action is not yet implemented")
def test_multiply():
    """This test is SKIPPED until the multiply action is built."""
    assert compute(5, "multiply") == 25


# ============================================================
# SECTION 4: Markers — @pytest.mark.skipif
# Use when a test should only run on a specific OS or condition.
# ============================================================

@pytest.mark.skipif(sys.platform == "win32", reason="Does not run on Windows")
def test_linux_only():
    """This test is SKIPPED on Windows; runs on Linux/Mac."""
    assert compute(3, "increment") == 4


# ============================================================
# SECTION 5: Markers — @pytest.mark.parametrize
# Run the SAME test function with MULTIPLE sets of input data.
# Each tuple = (value, action, expected_result)
# ============================================================

@pytest.mark.parametrize("value, action, expected", [
    (5,   "increment",  6),    # Case 1: basic increment
    (10,  "increment", 11),    # Case 2: another increment
    (10,  "decrement",  9),    # Case 3: basic decrement
    (0,   "decrement", -1),    # Case 4: decrement through zero
    (99,  "increment", 100),   # Case 5: large number
    (-5,  "increment", -4),    # Case 6: negative number
])
def test_compute_parametrized(value, action, expected):
    """
    Parametrized test — Pytest runs this 6 separate times,
    once for each tuple above.
    """
    assert compute(value, action) == expected


# ============================================================
# SECTION 6: Custom (User-Defined) Markers
# Group tests by purpose so you can run them selectively.
# Register these in pytest.ini:
#   [pytest]
#   markers =
#       smoke: Quick critical-path tests.
#       regression: Guard against previously fixed bugs.
#       slow: Long-running tests.
#
# Run selectively:
#   pytest -m smoke
#   pytest -m "not slow"
# ============================================================

@pytest.mark.smoke
def test_basic_smoke():
    """Smoke test: the most basic operation must work."""
    assert compute(1, "increment") == 2

@pytest.mark.regression
def test_regression_zero_decrement():
    """
    Regression: compute(0, 'decrement') previously returned 0
    instead of -1. This test guards against that bug returning.
    """
    assert compute(0, "decrement") == -1

@pytest.mark.slow
def test_large_loop():
    """Slow test: runs compute many times to check performance."""
    for i in range(10000):
        result = compute(i, "increment")
        assert result == i + 1


# ============================================================
# SECTION 7: Testing Flask API Routes with requests
#
# Prerequisite: Start the Flask app first in a separate terminal:
#   python app.py
#
# The app.py code (for reference):
#
#   from flask import Flask, request, jsonify
#   app = Flask(__name__)
#   students = []
#
#   @app.route('/students', methods=['GET'])
#   def get_students():
#       return jsonify(students), 200
#
#   @app.route('/students', methods=['POST'])
#   def add_student():
#       data = request.get_json()
#       students.append(data)
#       return jsonify({"message": "Student added", "student": data}), 201
#
#   if __name__ == '__main__':
#       app.run(debug=True, port=5000)
# ============================================================

BASE_URL = "http://127.0.0.1:5000"

@pytest.mark.skip(reason="Flask server must be running to test API routes")
def test_get_students_status_200():
    """GET /students → should return HTTP 200 OK."""
    response = requests.get(f"{BASE_URL}/students")
    assert response.status_code == 200

@pytest.mark.skip(reason="Flask server must be running to test API routes")
def test_get_students_returns_list():
    """GET /students → response body must be a JSON list."""
    response = requests.get(f"{BASE_URL}/students")
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.skip(reason="Flask server must be running to test API routes")
def test_post_student_status_201():
    """POST /students → should return HTTP 201 Created."""
    new_student = {"name": "Alice", "marks": 85}
    response = requests.post(f"{BASE_URL}/students", json=new_student)
    assert response.status_code == 201

@pytest.mark.skip(reason="Flask server must be running to test API routes")
def test_post_student_response_body():
    """POST /students → response body should confirm the added student."""
    new_student = {"name": "Bob", "marks": 70}
    response = requests.post(f"{BASE_URL}/students", json=new_student)
    body = response.json()

    assert "message" in body
    assert body["student"]["name"] == "Bob"
    assert body["student"]["marks"] == 70


# ============================================================
# HOW TO RUN THIS FILE
# ============================================================
#
#  Run all tests:
#    pytest testing.py -v
#
#  Run only tests matching "increment":
#    pytest testing.py -k "increment"
#
#  Run only smoke tests:
#    pytest testing.py -m smoke
#
#  Run all tests EXCEPT slow ones:
#    pytest testing.py -m "not slow" -v
#
# ============================================================
