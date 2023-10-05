from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqldb://''@host:3306/API_testing')
DatabaseSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
