import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:7486250@localhost:5432/esoft")

class Config:
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  
        