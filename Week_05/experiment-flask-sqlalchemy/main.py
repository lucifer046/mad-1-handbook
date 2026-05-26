# ── FLASK + SQLALCHEMY: THE POWER COUPLE ──
# Flask handles the Web requests. 
# SQLAlchemy handles the Database. 
# Together, they make a full-featured website!

import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# 1. Setup our path so the database file is saved in the right folder.
current_dir = os.path.abspath(os.path.dirname(__file__))

# 2. Initialize the Flask App.
app = Flask(__name__)

# 3. Tell Flask where our database file is.
# We are using SQLite, which is just a single file on our computer.
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "testdb.sqlite3") 

# 4. Initialize the Database extension.
db = SQLAlchemy()
db.init_app(app)

# We need to 'push' the app context so the database can "see" the app settings.
app.app_context().push()

# ── THE DATA BLUEPRINTS ──

class User(db.Model):
    """ Blueprint for a person. """
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)

class Article(db.Model):
    """ Blueprint for an article. """
    __tablename__ = 'article'
    article_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    
    # This automatically finds all Users linked to this Article through the bridge table.
    authors = db.relationship("User", secondary="article_authors")

class ArticleAuthors(db.Model):
    """ The Bridge Table: Connects Users to Articles. """
    __tablename__ = 'article_authors'
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("article.article_id"), primary_key=True) 

# ── THE ROUTES (The Service Counters) ──

@app.route("/", methods=["GET", "POST"])
def list_articles():
    if request.method == "GET":
        # We ask the database: "Give me EVERY article you have!"
        articles = Article.query.all() 
        return render_template("articles.html", articles=articles)

@app.route("/articles_by/<username>", methods=["GET", "POST"])
def articles_by_author(username):
    if request.method == "GET":        
        # We ask: "Give me articles where the author name matches what the user typed!"
        articles = Article.query.filter(Article.authors.any(username=username))
        return render_template("articles_by_author.html", articles=articles)

# Start the server!
if __name__ == '__main__':
    # host='0.0.0.0' means the website is accessible to anyone on your network.
    # port=8080 is the 'door number' for your website.
    app.run(host='0.0.0.0', debug=True, port=8080)
















