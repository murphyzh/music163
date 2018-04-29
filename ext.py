from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_URI


eng = create_engine(DB_URI)
print(eng)
Base = declarative_base()
Session = sessionmaker(bind=eng)
session = Session()

