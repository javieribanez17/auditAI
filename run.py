from flask import Flask, render_template, request, redirect, jsonify, url_for
import os
from dotenv import load_dotenv
from src.main import cleanCsv, agentAudit
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# userData = {
#             'user': 'Admin',
#             'password': 'Admin123'
#             }
isLogin = False

@app.route('/login', methods=['POST'])
def login():
    global isLogin
    newLogin = request.get_json()
    load_dotenv()
    boolUser = os.environ["user"] == newLogin['user']
    boolPassword = os.environ["password"] == newLogin['password']
    if(boolUser and boolPassword):
        isLogin = True
        return redirect(url_for('home'))
    else:
        message = "El usuario o contraseña no son validos"
        return jsonify({'error': message}), 401
    
@app.route('/home', methods=['GET'])
def home():
    global isLogin
    if isLogin is True:
        return render_template('home.html')
    else:
        return render_template('index.html')

@app.route('/', methods=['GET'])
def index():
    global isLogin
    isLogin = False
    return render_template('index.html')

@app.route('/gpt', methods=['POST'])
def agent():
    question = request.get_json()
    # gpt = question['question']
    gpt = agentAudit(question['question'])
    answer = {'answer': gpt}
    res = jsonify(answer)
    res.status_code = 200
    return res

@app.route('/upload', methods=['POST'])
def upload():
    nombres = []
    files = request.files.getlist('loadFile')
    for file in files:
        nombres.append(file.filename)
        extension = file.filename.split(".")[-1]
        name = file.filename.split(".")[0] 
        if 'AP' in name:
            file_path = './data/AP.csv'
            file.save(file_path)
        elif 'US' in name:
            file_path = './data/US.csv'
            file.save(file_path)
        elif 'CIE' or 'CUPS' or 'Tarifario' in name:
            file_path = './data/' + file.filename
            file.save(file_path)
        else:
            return render_template('error.html')
    cleanCsv()
    return render_template('ask.html', nombres=nombres)
