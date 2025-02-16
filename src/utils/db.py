'''Loads the connection string from the .env file and creates a database session'''

import os
import contextlib
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bank.bank_schema import ModelBase

load_dotenv()

DB_CONNECTION_STRING = str(os.getenv("DB_CONNECTION_STRING"))

engine = create_engine(DB_CONNECTION_STRING, echo=True)
ModelBase.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextlib.contextmanager
def get_db():
    '''Returns a database session'''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
