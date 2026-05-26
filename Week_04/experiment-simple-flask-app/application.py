# ── WELCOME TO THE BACKEND! ──
# Imagine you are the Manager of a Restaurant. 
# Flask is the system that helps you take orders and serve food.

from flask import Flask, render_template, request

# 1. We create the application instance.
# Think of this as opening the doors to your restaurant!
app = Flask(__name__)

# 2. We define a 'Route' (The Counter).
# When a customer visits the "/" path (the main entrance), 
# the 'index' function will run to handle their request.
@app.route("/", methods=["GET", "POST"])
def index():
    # A 'GET' request is like a customer just walking in to LOOK at the menu.
    if request.method == "GET":
        # We show them the form (the menu)
        return render_template("get_details.html")
    
    # A 'POST' request is like a customer SUBMITTING an order.
    if request.method == "POST":
        # We read what they typed in the box named 'name'
        user_name = request.form['name'] 
        
        # We prepare the result and serve it to them!
        return render_template("display_details.html", display_name=user_name)

# 3. Start the engine!
if __name__ == '__main__':
    # debug=True is like having a "Helper" who tells you exactly 
    # what went wrong if the stove stops working.
    app.run(debug=True)