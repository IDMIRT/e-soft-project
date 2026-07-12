from sqlalchemy import create_engine,select
from sqlalchemy.orm import sessionmaker, declarative_base
# from app.models import UploadedFiles,ResultAnalysis
# from config import DATABASE_URL

# DATABASE_URL = "postgresql://user:password@localhost:5432/mydatabase"
DATABASE_URL =  "postgresql://postgres:7486250@localhost:5432/esoft"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

Session = sessionmaker(bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def insert_record(data:dict,table_class,return_id=True):
    new_record = table_class(**data)
    session = Session()
    session.add(new_record)    
    session.commit()
    if return_id:
        return new_record.id
    

def view_result_analysis(id:int,table_class):
    
    try:
        session = Session()
        result = session.execute(select(table_class).where(table_class.fileload_id==id)) 

        record = result.first()[0]
        if record is not None:
            return {'mean':record.mean,'median':record.median,'correlation':record.correlation}
        else:
            return None
    finally:
        session.close()


def view_record_loadfiles(id:int, table_class):
    try:
        session = Session()
        result = session.execute(select(table_class).where(table_class.id==id)) 

        record = result.first()[0]
        if record is not None:
            return {'path':record.mean,'filename':record.filename}
        else:
            return None
    finally:
        session.close()


