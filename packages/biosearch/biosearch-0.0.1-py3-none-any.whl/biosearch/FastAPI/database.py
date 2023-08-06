import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

USER = os.environ.get('POSTGRESQL_USERNAME')
POSTGRESQL_PASSWORD = os.environ.get('PASSWORD', default='')
DOMAIN = 'localhost'
DATABASE = 'postgres'

SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{POSTGRESQL_PASSWORD}@{DOMAIN}/{DATABASE}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, expire_on_commit = False, autoflush=False, bind=engine) # creates the factory