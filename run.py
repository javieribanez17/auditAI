from flask import Flask, render_template, request, redirect, jsonify
import os
from src.main import cleanCsv, agentAudit
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/home', methods=['GET'])
def index():
    return redirect("/")

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

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
