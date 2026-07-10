from os import path
from flask import request, jsonify
import pandas as pd
from app.models import UploadedFiles,ResultAnalysis
from app.db import insert_record

APP_FOLDER = path.dirname(__file__).split('\\')[:-1]
UPLOADS_FOLDER = '\\'.join([*APP_FOLDER,'uploads'])

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
            
            try:
                data_uploads = {'path':UPLOADS_FOLDER,'filename':file.filename}
                id_record = insert_record(data_uploads,UploadedFiles,True)
            except Exception as e :
                return f"Ошибка при загрузке в БД"

        if dt.empty == False:
            mean = dt.mean(numeric_only=True).to_dict()
            median = dt.median(numeric_only=True).to_dict()
            correlation = dt.corr(numeric_only=True).to_dict()
            
            upload_analisis = {'fileload_id':id_record,'mean':mean,'median':median,'correlation':correlation}
            insert_record(upload_analisis,ResultAnalysis,False)            

    except:
        return "Ошибка загрузки файла",400  


    return f"Загрузка {file.filename} завершена",201
    


def stats():
    return f"Статистика"


def clean():
    return f"Очистка"
