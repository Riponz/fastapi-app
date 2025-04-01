from sqlalchemy import String, Integer, CHAR, Column
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4, UUID


Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    
    id = Column("id", String, default=str(uuid4()) , primary_key=True )
    title = Column("title", String)
    author = Column("author", String)
    genre = Column("genre", String)
    availability = Column("availability", Integer)
    
    def __init__(self, title, author, genre, availability):
        self.title = title
        self.author = author
        self.genre = genre
        self.availability = availability