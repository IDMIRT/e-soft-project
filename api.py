from flask import Flask,request
from os import path

app = Flask(__name__)

@app.route("/")
def start_page():
    return 'Стартовая страницы'

@app.route("/uploads/",methods = ['POST'])
def uploads_file():
    
    try:
        file = request.files['file']

        if file:
            # file.save('/uploads/'+file.filename)
            file.save('/uploads/testfile.csv')
            with open('/uploads/output.txt', 'w') as file:
                file.write("Это первая строка")
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
    
app.run(debug=True)