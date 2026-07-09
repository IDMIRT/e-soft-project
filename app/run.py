from db import engine, create_tables
# from models import UploadedFiles, ResultAnalysis
from flask import Flask
from api import start_page, test_page_number

errors = False

try:
    with engine.connect() as conn:        
        create_tables()
except Exception as ex:
    errors=True
    print(f"Ошибка подключения к БД")

if not(errors):
    app = Flask(__name__)
    # app.add_url_rule('/','start',start_page)
    # app.add_url_rule('/page/<int:number_page>','number_page',test_page_number)




    app.run(debug=False)
