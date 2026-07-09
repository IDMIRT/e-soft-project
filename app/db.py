from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

# DATABASE_URL = "postgresql://user:password@localhost:5432/mydatabase"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

Session = sessionmaker(bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def insert_record(data):
    pass

def list_records(table_name, limit=None):
    pass


