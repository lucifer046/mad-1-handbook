## Project Structure
```text
experiment-sqlalchemy/
 main.py
```

---

# Experiment 05: SQLAlchemy Basics
This experiment demonstrates the core principles of Object-Relational Mapping (ORM) using SQLAlchemy. Instead of writing raw SQL, we use Python classes to interact with the database.

## Detailed Code Breakdown

### 1. Library Imports
* `create_engine`: This is the starting point for any SQLAlchemy application. It handles the connection to the database (e.g., `sqlite:///./testdb.sqlite3`).
* `Column, Integer, String, ForeignKey`: These are schema building blocks. They define the type of data stored in each table column.
* `declarative_base`: This creates a `Base` class that all our models (User, Article) must inherit from so they are registered with SQLAlchemy.
* `relationship`: This is the magic of ORM. It allows us to access related data (like an article's authors) as if they were simple Python lists.

### 2. Model Definition
* `User`: Maps to the `user` table. Contains `user_id`, `username`, and `email`.
* `Article`: Maps to the `article` table. It has a `many-to-many` relationship with `User`.
* `ArticleAuthors`: This is a "Junction Table". Since one article can have many authors, and one user can write many articles, we need this table to link them via `user_id` and `article_id`.

### 3. Database Operations (The Transaction)
* `Session(eng)`: We open a session to start talking to the database.
* `sess.begin()`: Starts a transaction. This ensures that all operations either succeed together or fail together (Atomicity).
* `sess.query(User).filter(...)`: This generates a SQL `SELECT` statement behind the scenes to find specific users.
* `art.authors.append(u1)`: This is the beauty of ORM. We don't manually insert into the junction table; we just append a `User` object to the `Article`'s author list, and SQLAlchemy handles the rest during commit.
* `sess.commit()`: Finalizes the changes and writes them to the disk.
