## Project Structure
```text
experiment-sqlitedb/
 schema.sql
```

---

# Experiment 04: SQLite Database
This experiment covers the creation of a relational database structure using **SQLite**.

## Detailed Code Breakdown

### 1. Data Types
* `INTEGER PRIMARY KEY AUTOINCREMENT`: This tells SQLite to automatically generate a unique ID for every new row.
* `TEXT UNIQUE NOT NULL`: Ensures that the data (like email or username) must be provided and cannot be duplicated.

### 2. Relationships
* `FOREIGN KEY`: This is the backbone of relational databases. It "links" a column in one table to the primary key of another table.
* `PRIMARY KEY (user_id, article_id)`: In the junction table, we use a "Composite Primary Key". This ensures that the same user cannot be linked to the same article more than once.

### 3. Many-to-Many Pattern
* Since an article can have multiple authors, we don't store authors directly in the `article` table. Instead, we use the `article_authors` table to map the relationships between users and articles.
