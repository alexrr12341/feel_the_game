from flask import Flask, redirect, render_template, request, session, url_for,abort
from urllib.parse import parse_qs
import os
from Fortnite import *
from LoL import *
from eSport import *
from requests_oauthlib import OAuth1
app = Flask(__name__)
app.secret_key=str(os.system('openssl rand -base64 24'))
port=os.environ["PORT"]
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
    session['nombre']=jugador
    datosf=estadisticas_fortnite(plat,jugador)   
    session['victorias']=datosf[0]['Wins']
    session['kills']=datosf[0]['Kills'] 
    return render_template('fortnite.html',datosf=datosf,jugador=jugador)
@app.route('/leagueoflegends',methods=['POST'])
def procesar_lol():
    datos=request.form
    invocador=datos.get('invocador')
    region=datos.get('region')
    base=estadisticas_base(region,invocador)
    liga=obtener_ligas(region,invocador)
    session['invocador']=datos.get('invocador')
    try:
        if liga['Liga']==None:
            liga2=liga['Liga']+'UNRANKED'
        else:
            liga2=liga['Liga']
    except:
        liga2='UNRANKED'
    session['liga']=liga2
    session['victorias']=liga['Victorias']
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
@app.route('/metas/leagueoflegends',methods=['POST'])
def procesar_metas_lol():
    datos=request.form
    invocador=datos['invocador']
    region=datos['region']
    liga=datos['liga']
    nivel=datos['nivel']
    victorias=datos['victorias']
    liganum=dar_numero_liga(liga)
    datosl=obtener_ligas(region,invocador)
    liga2=datosl['Liga']
    liganum2=dar_numero_liga(liga2)
    victorias2=datosl['Victorias']
    datosl2=estadisticas_base(region,invocador)
    nivel2=datosl2['Nivel']
    resultadonivel=int(nivel)-int(nivel2)
    resultadovictorias=int(victorias)-int(victorias2)
    resultadoligas=int(liganum)-int(liganum2)
    return render_template('metaslol.html',resultadonivel=resultadonivel,resultadovictorias=resultadovictorias,resultadoligas=resultadoligas)
@app.route('/esports',methods=['POST','GET'])
def esports():
    torneo=sacar_torneo()
    enfrentamientos=conseguir_enfrentamientos()
    stream=obtener_enfrentamientos_lives()
    enfrentamientos_live=obtener_match_lives()
    return render_template('esports.html',torneo=torneo,enfrentamientos=enfrentamientos,stream=stream,enfrentamientos_live=enfrentamientos_live)
@app.route('/metas',methods=['POST','GET'])
def metas():
    return render_template('metas.html')
##PARTE TWITTER
REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHENTICATE_URL = "https://api.twitter.com/oauth/authenticate?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"
UPDATE_URL = 'https://api.twitter.com/1.1/statuses/update.json'
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
def get_request_token_oauth1():
    oauth = OAuth1(os.environ["CONSUMER_KEY"],
                  client_secret=os.environ["CONSUMER_SECRET"])
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    return credentials.get(b'oauth_token')[0],credentials.get(b'oauth_token_secret')[0]

def get_access_token_oauth1(request_token,request_token_secret,verifier):
    oauth = OAuth1(os.environ["CONSUMER_KEY"],
                   client_secret=os.environ["CONSUMER_SECRET"],
                   resource_owner_key=request_token,
                   resource_owner_secret=request_token_secret,
                   verifier=verifier,)
  
      
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    return credentials.get(b'oauth_token')[0],credentials.get(b'oauth_token_secret')[0]

@app.route('/twitter')
def twitter():
    request_token,request_token_secret = get_request_token_oauth1()
    authorize_url = AUTHENTICATE_URL + request_token.decode("utf-8")
    session["request_token"]=request_token.decode("utf-8")
    session["request_token_secret"]=request_token_secret.decode("utf-8")
    return redirect(authorize_url)

@app.route('/twitter_callback')
def twitter_callback():
    request_token=session["request_token"]
    request_token_secret=session["request_token_secret"]
    verifier  = request.args.get("oauth_verifier")
    access_token,access_token_secret= get_access_token_oauth1(request_token,request_token_secret,verifier)
    session["access_token"]= access_token.decode("utf-8")
    session["access_token_secret"]= access_token_secret.decode("utf-8")
    return redirect('/twittear')
@app.route('/twittear')
def twittear():
    try:
        invocador=session['invocador']
        liga=session['liga']
        victorias=session['victorias']
        update = '''Hola, mi nombre en el LeagueOfLegends es %s soy %s y tengo %s victorias de rankeds.
                    Mira tus estadísticas en:
                    https://feelthegame.herokuapp.com/'''%(invocador,liga,victorias)
    except:
        nombre=session['nombre']
        victorias=session['victorias']
        kills=session['kills']
        update = '''Hola, mi nombre en el Fortnite es %s tengo %s victorias y he hecho %s kills en total.
                    Mira tus estadísticas en:
                    https://feelthegame.herokuapp.com/'''%(nombre,victorias,kills)
    
    post = {"status": update}
    access_token=session["access_token"]
    access_token_secret=session["access_token_secret"]
    oauth = OAuth1(CONSUMER_KEY,client_secret=CONSUMER_SECRET,resource_owner_key=access_token,resource_owner_secret=access_token_secret)
    r=requests.post(UPDATE_URL, data=post, auth=oauth)
    if r.status_code==200:
        session.clear()
        return redirect('https://twitter.com/')
if __name__ == '__main__':
    port=os.environ["PORT"]
app.run('0.0.0.0',int(port), debug=True)