import requests
import os
import json
import codecs
def obtener_urlbase(region):
        URL_BASE='https://%s.api.riotgames.com/lol/'%region
        return URL_BASE
doc=json.load(codecs.open('CampeonesInfo.json', 'r', 'utf-8-sig'))
key=os.environ["keylol"]
URL_BASE='https://%s.api.riotgames.com/lol/'%region
parametros={'api_key':key,'locale':'es_ES'}
def obtener_id(region,invocador):
        URL_BASE=obtener_urlbase(region)
        r=requests.get(URL_BASE+'summoner/v4/summoners/by-name/'+'%s'%invocador,params=parametros)
        datos=r.json()
        if r.status_code==200:
                id=datos['id']
        else:
                print('Error en la Api')
        return id
def obtener_aid(region,invocador):
        URL_BASE=obtener_urlbase(region)
        r=requests.get(URL_BASE+'summoner/v4/summoners/by-name/'+'%s'%invocador,params=parametros)
        datos=r.json()
        if r.status_code==200:
                aid=datos['accountId']
        else:
                print('Error en la Api')
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
                print('Error en la Api')
def obtener_ligas(region,invocador):
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
                print('Error en la Api')
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
        else:
                print('Error en la Api')
def obtener_historial(region,invocador):
        URL_BASE=obtener_urlbase(region)
        aid=obtener_aid(region,invocador)
        y=requests.get(URL_BASE+'match/v4/matchlists/by-account/%s'%aid,params=parametros)
        datos4=y.json()
        listahistorialid=[]
        contadorh=1
        if y.status_code==200:
                for historial in datos4['matches']:
                        listahistorialid.append(historial['gameId'])
                        contadorh+=1
                        if contadorh>=5:
                                break
        else:
                print('Error en la Api')
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
                                kills=informacion['stats']['kills']
                                deaths=informacion['stats']['deaths']
                                assists=informacion['stats']['assists']
                                kda='%s/%s/%s'%(kills,deaths,assists)
                                dicchistorial['Nombre%i'%contadord]=diccnombres[idpar]
                                dicchistorial['Nivel%i'%contadord]=informacion['stats']['champLevel']
                                dicchistorial['Campeon%i'%contadord]=diccampeon[campeon2]
                                dicchistorial['KDA%i'%contadord]=kda
                                dicchistorial['Daño%i'%contadord]=informacion['stats']['totalDamageDealt']
                                dicchistorial['Vision%i'%contadord]=informacion['stats']['visionScore']
                                dicchistorial['Oro%i'%contadord]=informacion['stats']['goldEarned']
                                dicchistorial['Torretas%i'%contadord]=informacion['stats']['turretKills']
                                dicchistorial['Inhibidor%i'%contadord]=informacion['stats']['inhibitorKills']
                                dicchistorial['Victoria%i'%contadord]=informacion['stats']['win']
                                contadord+=1
                                if contadord>10:
                                        contadord-=9
                        listahistorial.append(dicchistorial.copy())
                else:
                        print('Error en la Api')
        return listahistorial