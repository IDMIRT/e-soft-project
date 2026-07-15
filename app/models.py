from sqlalchemy import Column, Integer, String, DateTime,ForeignKey,Float,JSON
from app.db import Base
from datetime import datetime

class UploadedFiles(Base):
    __tablename__= 'uploaded_files'
    id = Column(Integer, primary_key=True)
    data_load = Column(DateTime,default=datetime.now)
    path = Column(String(256))
    filename = Column(String())
    

class ResultAnalysis(Base):
    __tablename__='result_analysis'
    id = Column(Integer,primary_key=True)
    fileload_id=Column(ForeignKey('uploaded_files.id'))     
    mean = Column(JSON)
    median = Column(JSON)
    correlation = Column(JSON)



