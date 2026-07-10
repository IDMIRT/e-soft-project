from app.db import engine, create_tables
from flask import Flask
from app.api import uploads_file
from os import path
from pathlib import Path

errors = False


APP_FOLDER = path.dirname(__file__)
UPLOADS_FOLDER = path.join(APP_FOLDER, 'uploads')


upload_path = Path(UPLOADS_FOLDER)
if path.isdir(upload_path):
    upload_path.mkdir(parents=True, exist_ok=True)

try:
    with engine.connect() as conn:        
        create_tables()
except Exception as ex:
    errors=True
    print(f"Ошибка подключения к БД")

if not(errors):
    app = Flask(__name__)
    app.add_url_rule('/upload','upload',uploads_file,methods = ['POST','GET'])
    # app.add_url_rule('/page/<int:number_page>','number_page',test_page_number)
    app.run(debug=False)
