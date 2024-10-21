from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#import os

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:banco@localhost:5432/teste"
# SQLALCHEMY_DATABASE_URL = "postgresql://" + os.environ["DB_USER"] + ":" + os.environ["DB_PASS"] + "@" + os.environ["DB_HOST"] + ":5432/escola"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()