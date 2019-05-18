from flask import Flask, redirect, render_template, request, session, url_for,abort
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
    return render_template('fortnite.html',datosf=datosf,jugador=jugador)
@app.route('/leagueoflegends',methods=['POST'])
def procesar_lol():
    datos=request.form
    invocador=datos['invocador']
    region=datos['region']
    base=estadisticas_base(region,invocador)
    liga=obtener_ligas(region,invocador)
    liga2=str
    try:
        #Esto es la mayor tonteria que he hecho en programación.
        if liga['Liga']==None:
            liga2=liga['Liga']+'UNRANKED'
        else:
            liga2=liga['Liga']
    except:
        liga2='UNRANKED'
    maestrias=obtener_maestrias(region,invocador)
    historial=obtener_historial(region,invocador)
    return render_template('leagueoflegends.html',base=base,invocador=invocador,liga=liga,maestrias=maestrias,historial=historial,liga2=liga2)
@app.route('/metas/fortnite',methods=['POST'])
def procesar_metas_fortnite():
    datos=request.form
    plat=datos['plataforma']
    jugador=datos['cuenta']
    datosf=estadisticas_fortnite(plat,jugador)
    resultadokills=int(datos['kills2'])-int(datosf[0]['Kills'])
    resultadovictorias=int(datos['victorias2'])-int(datosf[0]['Wins'])
    resultadopartidas=int(datos['partidas2'])-int(datosf[0]['Matches Played'])
    resultadopuntuacion=float(datos['puntuacion2'])-float(datosf[0]['Score'].replace(",","."))
    return render_template('metasfortnite.html',resultadokills=resultadokills,resultadovictorias=resultadovictorias,resultadopartidas=resultadopartidas,resultadopuntuacion=resultadopuntuacion)

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