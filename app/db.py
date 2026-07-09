from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

# DATABASE_URL = "postgresql://user:password@localhost:5432/mydatabase"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

Session = sessionmaker(bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def insert_record(data:dict,table_class):
    new_record = table_class(**data)
    session = Session()
    session.add(new_record)    
    session.commit()
    return new_record.id

def list_records(table_name, limit=None):
    pass


