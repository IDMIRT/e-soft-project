from sqlalchemy import Column, Integer, String, Text, DateTime,ForeignKey,Float
from sqlalchemy.orm import declarative_base
from db import Base
from datetime import datetime

class UploadedFiles(Base):
    __tablename__= 'uploaded_files'
    id = Column(Integer, primary_key=True)
    data_load = Column(DateTime,default=datetime.now)
    path = Column(String(256))
    filename = Column(String())
    # filedata = Column(Text())

class ResultAnalysis(Base):
    _tablename_='result_analysis'
    id = Column(Integer,primary_key=True)
    fileload_id=Column(ForeignKey('uploaded_files.id')) 
    ColumnName = Column(String())
    ColumnMean = Column(Float())
    ColumnMedian = Column(Float())
    ColumnCorrelation = Column(Float())



