# ── WELCOME TO THE MAGIC OF ORM! ──
# "ORM" (Object-Relational Mapping) is like a Translator. 
# It translates Python "Objects" into Database "Rows". 
# You talk in Python, and it talks in SQL for you!

import sqlalchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session, declarative_base, relationship

# 1. THE BASE: Every blueprint (class) needs a starting point.
Base = declarative_base()

# 2. THE BLUEPRINTS (Models)
# Imagine these are the 'Rules' for our Excel sheets.

class User(Base):
    """ Represents a person in our system. """
    __tablename__ = 'user'
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)

class Article(Base):
    """ Represents a story or post. """
    __tablename__ = 'article'
    article_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    content = Column(String)
    
    # THE MAGIC LINK: 
    # secondary="article_authors" tells SQLAlchemy to use the bridge table 
    # to find who wrote this article.
    authors = relationship("User", secondary="article_authors")

class ArticleAuthors(Base):
    """ THE BRIDGE: Connects Users to Articles. """
    __tablename__ = 'article_authors'
    user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    article_id = Column(Integer, ForeignKey("article.article_id"), primary_key=True) 

# 3. THE ENGINE: This is the 'Driver' that connects Python to the SQLite file.
engine = create_engine("sqlite:///./testdb.sqlite3")

if __name__ == '__main__':
    # 4. THE SESSION: This is like a 'Phone Call' to the database.
    # Everything we do inside the 'with' block happens in one conversation.
    with Session(engine) as session:
        try:
            # We are asking the Translator (ORM) to find two users for us.
            user1 = session.query(User).filter(User.username == "alice").one()
            user2 = session.query(User).filter(User.username == "bob").one()

            # We create a NEW Article object in Python.
            new_article = Article(
                title="Learning ORM is Fun!", 
                content="SQLAlchemy makes databases easy to use!"
            )

            # WE JUST APPEND THE USERS! 
            # We don't have to write any SQL INSERT commands. 
            # SQLAlchemy will see this and update the 'Bridge' table for us!
            new_article.authors.append(user1)
            new_article.authors.append(user2)
            
            # Tell the session to 'track' this new article
            session.add(new_article)
            
            # 5. COMMIT: This is like clicking 'SAVE' in a video game.
            # If we don't commit, our changes are lost when the program ends.
            session.commit()
            print("Successfully saved the article and linked its authors!")

        except Exception as e:
            # If the stove catches fire, we STOP and ROLL BACK.
            # This undoes any half-finished changes to keep the data safe.
            print(f"Oops! Something went wrong: {e}")
            session.rollback()

















