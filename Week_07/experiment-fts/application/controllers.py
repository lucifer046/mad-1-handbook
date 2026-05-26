# request: To access URL query parameters (like /search?q=flask)
# current_app as f_app: Accesses the globally active Flask app instance
from flask import request, render_template, current_app as f_app
# Article: The standard DB model
# ArticleSearch: A virtual table model used for SQLite Full-Text Search (FTS)
from application.models import Article, ArticleSearch

@f_app.route("/", methods=["GET", "POST"])
def list_articles():
    f_app.logger.info("Fetching all articles...")
    # arts: list of Article objects
    arts = Article.query.all()    
    return render_template("articles.html", articles=arts)

@f_app.route("/articles_by/<u_name>", methods=["GET", "POST"])
def articles_by_author(u_name): # u_name: user_name
    # Filter articles by the provided username
    arts = Article.query.filter(Article.authors.any(username=u_name))
    return render_template("articles_by_author.html", articles=arts, username=u_name)

@f_app.route("/search", methods=["GET"])
def perform_search():
    # Get search query 'q' from URL parameters
    query = request.args.get('q') # query: search_term
    
    # Perform Full-Text Search using the MATCH operator
    # res: search_results
    res = ArticleSearch.query.filter(ArticleSearch.content.op("MATCH")(query)).all()    
    
    f_app.logger.debug(f"Search results for '{query}': {len(res)} items found.")
    return render_template("results.html", q=query, results=res)
