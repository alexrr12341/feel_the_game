from flask import Flask, redirect, render_template, request, session, url_for
from urllib.parse import parse_qs
import os
from Fortnite import *
from LoL import *
app = Flask(__name__)
@app.route('/',methods=['POST','GET'])
def inicio():
    listat=tienda_fortnite()
    listal=obtener_rotacion()
    return render_template('index.html',listat=listat,listal=listal)
@app.route('/estadisticas',methods=['POST','GET'])
def estadisticas():
    return render_template('estadisticas.html')
@app.route('/fortnite',methods=['POST'])
def procesar_fortnite():
    datos=request.form
    plat=datos['plataforma']
    jugador=datos['cuenta']
    datosf=estadisticas_fortnite(plat,jugador)
    return render_template('fortnite.html',datos=datosf)
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