from os import path
from flask import request, jsonify,send_file
import pandas as pd
from app.models import UploadedFiles,ResultAnalysis
from app.db import insert_record,view_result_analysis,view_record_loadfiles
import matplotlib
import matplotlib.pyplot as plt

APP_FOLDER = path.dirname(__file__).split('\\')[:-1]
UPLOADS_FOLDER = '\\'.join([*APP_FOLDER,'uploads'])

file_path = None

def load_file_pandas(file_path):
    if file_path.endswith('.csv'):
        dt = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx") or file_path.endswith(".xls") : 
        dt = pd.read_excel(file_path)
    else: 
        dt = None        
    return dt


def uploads_file():
   
    try:
        if 'file' not in request.files:
            return jsonify({'error':f"Нет файла"}),401
        

        file = request.files['file']

        if file:
            file_path = path.join(UPLOADS_FOLDER, file.filename)
            file.save(file_path)
        else:
            raise FileExistsError('Ошибка, не передан файл')

        if file_path:
            dt = load_file_pandas(file_path) 
            if dt is None:
                return f"Неподдерживаемый тип файла, используйте файлы с расширением csv, xls или xlsx",415            
            
            try:
                data_uploads = {'path':UPLOADS_FOLDER,'filename':file.filename}
                id_record = insert_record(data_uploads,UploadedFiles,True)
            except Exception as e :
                return f"Ошибка при загрузке в БД",506

        if dt.empty == False:
            mean = dt.mean(numeric_only=True).to_dict()
            median = dt.median(numeric_only=True).to_dict()
            correlation = dt.corr(numeric_only=True).to_dict()
            
            upload_analisis = {'fileload_id':id_record,'mean':mean,'median':median,'correlation':correlation}
            insert_record(upload_analisis,ResultAnalysis,False)            

    except:
        return jsonify({'message':f"Ошибка загрузки файла"}),507  


    return jsonify({'message':f"Загрузка {file.filename} завершена"}),200   
    


def stats(id):
    """Получаем данные из таблицы ResultAnalysis
    id - id записи в таблице"""
    result_stats = view_result_analysis(id,ResultAnalysis) 

    if result_stats is not None:
        return jsonify({
        'mean': result_stats['mean'],
        'median': result_stats['median'],
        'correlation': result_stats['correlation']
    }), 200 
    else:
        return jsonify({'message':f"Данные не найдены"}),404


def clean(id):
    Cleaned = False
    data = view_record_loadfiles(id,UploadedFiles)
    
    if data is not None:
        file = path.join(data['path'], data['filename'])
    else:
        return jsonify({'message':f"Данные не найдены"}),404
    
    try:
        if path.isfile(file):

            dt = load_file_pandas(file)
            if dt is not None:

                dt.drop_duplicates(inplace=True)
                dt.fillna(0, inplace=True)
                Cleaned = True

                if file.endswith('.csv'):  
                    dt.to_csv(file,index=False)
                else:
                    dt.to_excel(file.xlsx,index=False)

        if Cleaned == True:
            return jsonify({'message':f'Очистка данных завершена'}), 201
        else:
            return jsonify({'message':f'Ошибка при очистке'}),505
        
    except Exception as e:
        return jsonify({f'Ошибка': str(e)}), 400


def plot(id:int):
    matplotlib.use('Agg')
    data = view_record_loadfiles(id,UploadedFiles) 

    if data is not None:
        file = path.join(data['path'], data['filename']) 
    else:
        return jsonify({'message':f"Данные не найдены"}),404
    
    try:
        if path.isfile(file):

            dt = load_file_pandas(file)

            if dt is not None:
                plt.figure(figsize=(10, 6))
                dt.plot()
                path_save = path.join(UPLOADS_FOLDER, f"plot_{id}.png")
                plt.savefig(path_save)
                plt.close()  

        

        return send_file(path_save, mimetype='image/png')

    except Exception as e:
        return jsonify({f'Ошибка': str(e)}), 400
    
    
    
