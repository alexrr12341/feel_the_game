import requests
import os
import json
import codecs
def obtener_urlbase(region):
        URL_BASE='https://%s.api.riotgames.com/lol/'%region
        return URL_BASE
doc=json.load(codecs.open('CampeonesInfo.json', 'r', 'utf-8-sig'))
key=os.environ["keylol"]
region=str(input("¿Cual es tu region? (euw,na...) "))
URL_BASE='https://%s.api.riotgames.com/lol/'%region
parametros={'api_key':key,'locale':'es_ES'}
invocador=str(input("¿Cual es el nombre de invocador? "))

def obtener_id(region,invocador):
        URL_BASE=obtener_urlbase(region)
        r=requests.get(URL_BASE+'summoner/v4/summoners/by-name/'+'%s'%invocador,params=parametros)
        datos=r.json()
        if r.status_code==200:
                id=datos['id']
        else:
                print('Error en la Api')
        return id
def obtener_aid(region,invcoador):
        URL_BASE=obtener_urlbase(region)
        r=requests.get(URL_BASE+'summoner/v4/summoners/by-name/'+'%s'%invocador,params=parametros)
        datos=r.json()
        if r.status_code==200:
                aid=datos['accountId']
        else:
                print('Error en la Api')
        return id

def estadisticas_base(region,invocador):
        URL_BASE=obtener_urlbase(region)
        r=requests.get(URL_BASE+'summoner/v4/summoners/by-name/'+'%s'%invocador,params=parametros)
        datos=r.json()
        if r.status_code==200:
                print('Nombre:',datos['name'])
                print('Nivel de invocador:',datos['summonerLevel'])
                print('Icono de Invocador:',datos['profileIconId'])
        else:
                print('Error en la Api')
print(estadisticas_base(region,invocador))

def obtener_ligas(region,invocador):
        id=obtener_id(region,invocador)
        s=requests.get(URL_BASE+'league/v4/entries/by-summoner/'+'%s'%id,params=parametros)
        datos2=s.json()
        if s.status_code==200:
                for info in datos2:
                        print('Liga:',info['tier'])
                        print('Rango:',info['rank'])
                        print('Victorias:',info['wins'])
                        print('Derrotas:',info['losses'])
        else:
                print('Error en la Api')
print(obtener_ligas(region,invocador))
def obtener_maestrias(region,invocador):
        URL_BASE=obtener_urlbase(region)
        id=obtener_id(region,invocador)
        t=requests.get(URL_BASE+'champion-mastery/v4/champion-masteries/by-summoner/%s'%id,params=parametros)
        datos3=t.json()
        contador=0
        listacampeones=[]
        for campeones in doc['data']:
                listacampeones.append(campeones)
        diccampeon={}
        for campeones in listacampeones:
                ids=doc['data'][campeones]['key']
                diccampeon[ids]=doc['data'][campeones]['id']
        print('Maestrias de campeones')
        if t.status_code==200:
                for maestrias in datos3:
                                #Esto lo hago por si el campeon no esta en la lista, al ser un texto plano puede estar desactualizada la información que da League of Legends
                        try:
                                idc=maestrias['championId']
                                idc2=str(idc)
                                print('Campeon :',diccampeon[idc2])
                                print('Puntos de Maestria :',maestrias['championPoints'])
                                print('Nivel de Campeon :',maestrias['championLevel'])
                                contador+=1
                                if contador>=5:
                                        break
                        except:
                                contador-=1
        else:
                print('Error en la Api')
print(obtener_maestrias(region,invocador))

def obtener_historial(region,invocador):
        URL_BASE=obtener_urlbase(region)
        aid=obtener_aid(region,invocador)
        y=requests.get(URL_BASE+'match/v4/matchlists/by-account/%s'%aid,params=parametros)
        datos4=y.json()
        listahistorialid=[]
        contadorh=0
        if y.status_code==200:
                for historial in datos4['matches']:
                        listahistorialid.append(historial['gameId'])
                        contadorh+=1
                        if contadorh>=5:
                                break
        else:
                print('Error en la Api')
        contadorH=1
        contadorVs=0
        listakda=[]
        contadorkda=0
        diccnombres={}
        for historialid in listahistorialid:
                print("")
                print('Historial',contadorH)
                print("")
                contadorH+=1
                u=requests.get(URL_BASE+'match/v4/matches/%s'%historialid,params=parametros)
                datos5=u.json()
                if u.status_code==200:
                        for infoids in datos5['participantIdentities']:
                                idsc=infoids['participantId']
                                diccnombres[idsc]=infoids['player']['summonerName']
                        for informacion in datos5['participants']:
                                print("")
                                idpar=informacion['participantId']
                                campeon=informacion['championId']
                                campeon2=str(campeon)
                                print('Participante:',diccnombres[idpar])
                                print('Nivel',informacion['stats']['champLevel'])
                                print('Campeon',diccampeon[campeon2])
                                print('KDA:',informacion['stats']['kills'],'/',informacion['stats']['deaths'],'/',informacion['stats']['assists'])
                                print('Daño total',informacion['stats']['totalDamageDealt'])
                                print('Vision',informacion['stats']['visionScore'])
                                print('Oro Conseguido',informacion['stats']['goldEarned'])
                                print('Torretas destruidas',informacion['stats']['turretKills'])
                                print('Inhibidores destruidos',informacion['stats']['inhibitorKills'])
                                print('Victoria:',informacion['stats']['win'])
                else:
                        print('Error en la Api')
print(obtener_aid(region,invocador))