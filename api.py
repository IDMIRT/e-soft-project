from flask import Flask,request,jsonify
from os import path

APP_FOLDER = path.dirname(__file__)
UPLOADS_FOLDER = path.join(APP_FOLDER, 'uploads')

app = Flask(__name__)

@app.route("/")
def start_page():
    return 'Стартовая страницы'

@app.route("/uploads",methods = ['POST','GET'])
def uploads_file():
    # file_path = path.join(APP_FOLDER, 'uploads', 'output.txt')
    # with open(file_path, 'w',encoding='utf-8') as file:
    #         file.write("Это первая строка")
    try:
        if 'file' not in request.files:
            return jsonify({'error':"No File Part"}),401
        

        file = request.files['file']

        if file:
            # file.save('/uploads/'+file.filename)
            file_path = path.join(UPLOADS_FOLDER, file.filename)
            file.save(file_path)
            # with open('/uploads/output.txt', 'w') as file:
                # file.write("Это первая строка")
        else:
            raise FileExistsError('Ошибка, не передан файл')    
    except:
        return "Ошибка загрузки файла",400  


    return f"Загрузка {file.filename} завершена",201

@app.route("/data/stats",methods = ['GET'])
def stats():
    pass


@app.route("/data/clean",methods = ['POST'])
def clean():
    pass
    
app.run()