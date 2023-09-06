from flask import Flask, request
import os
from main import agentAudit
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def home():
    return "Hola mundo"

@app.route('/gpt', methods=['GET'])
def agent():
    return agentAudit()

# @app.route('/upload', methods=['POST'])
# def upload():
#     if(len(os.listdir("./data")) == 1):
#         deleteFile()
#     global file_path
#     file = request.files['file']
#     extension = file.filename.split(".")[-1]
#     if extension in extensions:
#         file_path = './data/data.' + extension
#         file.save(file_path)
#         return "", 201
#     else:
#         raise Exception("Archivo no valido")

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