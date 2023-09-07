from flask import Flask, request
import os
from src.main import agentAudit
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def home():
    return "Hola mundo"

@app.route('/gpt', methods=['GET'])
def agent():
    return agentAudit()

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('archivos')
    for file in files:
        extension = file.filename.split(".")[-1]
        if extension == "csv":
            file_path = './data/data.' + file.filename
            file.save(file_path)
        else:
            raise Exception("Archivo no valido")
    return "", 201
    
# @app.route('/xlsx', methods=['POST'])
# def read_xlsx():
#     question = request.get_json()
#     answer = xlsx(file_path, question['content'])
#     return answer

# @app.route('/pdf', methods=['POST'])
# def read_pdf():
#     question = request.get_json()
#     answer = pdfs(file_path, question['content'])
#     return answer


# @app.route('/', methods=['DELETE'])
# def deleteFile():
#     global file_path
#     try:
#         os.remove(file_path)
#     except Exception as e:
#         print(e)
#     return '', 204

# @app.route('/connect', methods=['POST'])
# def read_db():
#     datos_formulario = request.get_json()
#     conect_db(datos_formulario)
#     return "", 201

# @app.route('/db', methods=['POST'])
# def ask_db():
#     question = request.get_json()
#     answer = db(question['content'])
#     return answer