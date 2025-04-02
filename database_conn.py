from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

engine = create_engine("sqlite:///books.db", echo=True)

Base.metadata.create_all(bind=engine)

db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)