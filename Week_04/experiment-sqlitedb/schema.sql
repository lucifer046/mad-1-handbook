-- ── THE DATABASE SKELETON ──
-- Imagine a database as a big, super-smart Excel file.
-- These commands tell the computer how to build the "Sheets".

-- 1. Create the 'user' sheet
-- Every student gets a unique 'user_id' so we don't mix them up!
CREATE TABLE user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT, -- A unique ID that counts up automatically
    username TEXT UNIQUE NOT NULL,             -- Cannot be empty, cannot be a duplicate
    email TEXT UNIQUE NOT NULL
);

-- 2. Create the 'article' sheet
-- This is where the stories/articles are stored.
CREATE TABLE article (
    article_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

-- 3. THE BRIDGE (Junction Table)
-- Sometimes, many users can write many articles. 
-- This table is the "Bridge" that connects them using their IDs.
CREATE TABLE article_authors (
    user_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    
    PRIMARY KEY (user_id, article_id), -- Together, these two IDs make a unique pair
    
    -- These are 'Foreign Keys'. They point back to the original tables.
    -- Think of them as "Check the User ID in the user sheet".
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (article_id) REFERENCES article(article_id)
);
