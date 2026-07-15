from app.db import engine, create_tables
from flask import Flask
from app.api import uploads_file,stats,clean,plot
from os import path
from pathlib import Path

errors = False


APP_FOLDER = path.dirname(__file__)
UPLOADS_FOLDER = path.join(APP_FOLDER, 'uploads')


upload_path = Path(UPLOADS_FOLDER)
if not path.isdir(upload_path):
    upload_path.mkdir(parents=True, exist_ok=True)

try:
    with engine.connect() as conn:        
        create_tables()
except Exception as ex:
    errors=True
    print(f"Ошибка подключения к БД")

if not errors:
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.add_url_rule('/upload','upload',uploads_file,methods = ['POST','GET'])
    app.add_url_rule('/stats/<int:id>','stats',stats)
    app.add_url_rule('/clean/<int:id>','clean',clean)
    app.add_url_rule('/plot/<int:id>','plot',plot)
    
    app.run(debug=False)
