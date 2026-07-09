from os import path
from flask import request, jsonify
import pandas as pd
from models import UploadedFiles,ResultAnalysis
from db import insert_record
# from datetime import datetime


APP_FOLDER = path.dirname(__file__)
UPLOADS_FOLDER = path.join(APP_FOLDER, 'uploads')


# def start_page():
#     return 'Стартовая страницы'

# def test_page_number(number_page:str):
#     return f'Страница с номером {number_page}'
file_path = None


def uploads_file():
   
    try:
        if 'file' not in request.files:
            return jsonify({'error':"Нет файла"}),401
        

        file = request.files['file']

        if file:
            file_path = path.join(UPLOADS_FOLDER, file.filename)
            file.save(file_path)
        else:
            raise FileExistsError('Ошибка, не передан файл') 

        if file_path:
            if file_path.endswith('.csv'):
                dt = pd.read_csv(file_path)
            elif file_path.endswith(".xlsx") or ".xls": 
                dt = pd.read_excel(file_path)
            else: 
                return f"Неизвестный тип файла, используйте csv, xls или xlsx"
            
            data_uploads = {'path':UPLOADS_FOLDER,'file':file.filename}
            id_record = insert_record(data_uploads,UploadedFiles)

        if dt.empty == False:
            mean = dt.mean(numeric_only=True).to_dict()
            median = dt.median(numeric_only=True).to_dict()
            correlation = dt.corr(numeric_only=True).to_dict()

            

    except:
        return "Ошибка загрузки файла",400  


    return f"Загрузка {file.filename} завершена",201
    # return f"Загрузка файлов"


def stats():
    return f"Статистика"


def clean():
    return f"Очистка"
