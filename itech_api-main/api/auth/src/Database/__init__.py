from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(getenv("DB_DNS"), echo=True)
DatabaseSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
