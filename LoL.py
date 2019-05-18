import requests
import os
import json
import codecs
from flask import abort
doc=json.load(codecs.open('CampeonesInfo.json', 'r', 'utf-8-sig'))
doc2=json.load(codecs.open('Summoners.json', 'r', 'utf-8-sig'))
key=os.environ["keylol"]
parametros={'api_key':key,'locale':'es_ES'}
def obtener_urlbase(region):
        URL_BASE='https://%s.api.riotgames.com/lol/'%region
        return URL_BASE
def obtener_rotacion():
        #Ponemos esta URL ya que las rotaciones no cambian
        t=requests.get('https://euw1.api.riotgames.com/lol/platform/v3/champion-rotations',params=parametros)
        datos=t.json()
        listacampeones=[]
        diccampeon={}
        listacampeones2=[]
        for campeones in doc['data']:
                listacampeones.append(campeones)
        for campeones in listacampeones:
                ids=doc['data'][campeones]['key']
                diccampeon[ids]=doc['data'][campeones]['id']
        if t.status_code==200:
                for ids in datos['freeChampionIds']:
                        ids2=str(ids)
                        listacampeones2.append(diccampeon[ids2])
                return listacampeones2    
        else:
                abort(404)          
def obtener_id(region,invocador):
        URL_BASE=obtener_urlbase(region)
        r=requests.get(URL_BASE+'summoner/v4/summoners/by-name/'+'%s'%invocador,params=parametros)
        datos=r.json()
        if r.status_code==200:
                id=datos['id']
        else:
                abort(404)
        return id
def obtener_aid(region,invocador):
        URL_BASE=obtener_urlbase(region)
        r=requests.get(URL_BASE+'summoner/v4/summoners/by-name/'+'%s'%invocador,params=parametros)
        datos=r.json()
        if r.status_code==200:
                aid=datos['accountId']
        else:
                abort(404)
        return aid
def estadisticas_base(region,invocador):
        URL_BASE=obtener_urlbase(region)
        r=requests.get(URL_BASE+'summoner/v4/summoners/by-name/'+'%s'%invocador,params=parametros)
        datos=r.json()
        diccbase={}
        if r.status_code==200:
                diccbase['Nombre']=datos['name']
                diccbase['Nivel']=datos['summonerLevel']
                diccbase['Icono']=datos['profileIconId']
                return diccbase
        else:
                abort(404)
def obtener_ligas(region,invocador):
        URL_BASE=obtener_urlbase(region)
        id=obtener_id(region,invocador)
        s=requests.get(URL_BASE+'league/v4/entries/by-summoner/'+'%s'%id,params=parametros)
        datos2=s.json()
        diccligas={}
        if s.status_code==200:
                for info in datos2:
                        diccligas['Liga']=info['tier']
                        diccligas['Rango']=info['rank']
                        diccligas['Victorias']=info['wins']
                        diccligas['Derrotas']=info['losses']
                        return diccligas
        else:
                abort(404)
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
        if t.status_code==200:
                listamaestrias=[]
                diccmaestrias={}
                for maestrias in datos3:
                        idc=maestrias['championId']
                        idc2=str(idc)
                        diccmaestrias['Campeon']=diccampeon[idc2]
                        diccmaestrias['Puntos']=maestrias['championPoints']
                        diccmaestrias['Nivel']=maestrias['championLevel']
                        listamaestrias.append(diccmaestrias.copy())
                        contador+=1
                        if contador>=5:
                                break
                        
                return listamaestrias  
        #No hago abort 404 ya que sino tienes maestrias podrás buscar tu información basica igual.

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
        #No hago abort 404 ya que sino tienes historial podrás buscar tu información basica igual.

        listakda=[]
        contadorkda=0
        diccnombres={}
        diccampeon={}
        listacampeones=[]
        dicchistorial={}
        contadord=1
        listahistorial=[]
        for campeones in doc['data']:
                listacampeones.append(campeones)
        diccampeon={}
        for campeones in listacampeones:
                ids=doc['data'][campeones]['key']
                diccampeon[ids]=doc['data'][campeones]['id']
        for historialid in listahistorialid:
                u=requests.get(URL_BASE+'match/v4/matches/%s'%historialid,params=parametros)
                datos5=u.json()
                if u.status_code==200:
                        for infoids in datos5['participantIdentities']:
                                idsc=infoids['participantId']
                                diccnombres[idsc]=infoids['player']['summonerName']
                        for informacion in datos5['participants']:
                                idpar=informacion['participantId']
                                campeon=informacion['championId']
                                campeon2=str(campeon)
                                if diccnombres[idpar]==invocador:
                                        kills=informacion['stats']['kills']
                                        deaths=informacion['stats']['deaths']
                                        assists=informacion['stats']['assists']
                                        kda='%s/%s/%s'%(kills,deaths,assists)
                                        dicchistorial['Nombre']=diccnombres[idpar]
                                        dicchistorial['Nivel']=informacion['stats']['champLevel']
                                        dicchistorial['Campeon']=diccampeon[campeon2]
                                        dicchistorial['KDA']=kda
                                        dicchistorial['Item0']=informacion['stats']['item0']
                                        dicchistorial['Item1']=informacion['stats']['item1']
                                        dicchistorial['Item2']=informacion['stats']['item2']
                                        dicchistorial['Item3']=informacion['stats']['item3']
                                        dicchistorial['Item4']=informacion['stats']['item4']
                                        dicchistorial['Item5']=informacion['stats']['item5']
                                        dicchistorial['Item6']=informacion['stats']['item6']
                                        dicchistorial['Daño']=informacion['stats']['totalDamageDealt']
                                        dicchistorial['Vision']=informacion['stats']['visionScore']
                                        dicchistorial['Oro']=informacion['stats']['goldEarned']
                                        dicchistorial['Victoria']=informacion['stats']['win']
                                        listahistorial.append(dicchistorial.copy())
                else:
                        abort(404)
        return listahistorial