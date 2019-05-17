from flask import Flask, redirect, render_template, request, session, url_for
from urllib.parse import parse_qs
import os
app = Flask(__name__)
@app.route('/',methods=['POST','GET'])
def inicio():
    return render_template('index.html')
@app.route('/estadisticas',methods=['POST','GET'])
def estadisticas():
    return render_template('estadisticas.html')
@app.route('/esports',methods=['POST','GET'])
def esports():
    return render_template('esports.html')
@app.route('/guias',methods=['POST','GET'])
def guias():
    return render_template('guias.html')
@app.route('/metas',methods=['POST','GET'])
def metas():
    return render_template('metas.html')
app.run(debug=True)