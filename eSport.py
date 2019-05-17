import os
import requests
key=os.environ['keypanda']
parametros={'token':key}
URL_BASE='https://api.pandascore.co'
r=requests.get(URL_BASE+'//lol/tournaments/running',params=parametros)
datos=r.json()
diccequipos={}
dicctorneo={}
def sacar_torneo():
        for torneos in datos:
                torneo=torneos['league']['name'].capitalize()
                imagen=torneos['league']['image_url']
                dicctorneo['Nombre']=torneo
                dicctorneo['Imagen']=imagen
        return dicctorneo
def conseguir_enfrentamientos():
        diccequiposT={}
        listaequipos=[]
        diccequipos2={}
        for torneos in datos:
                for equipos in torneos['teams']:
                        id=equipos['id']
                        id2=str(id)
                        diccequipos[id2]=equipos['name']
                for partidas in torneos['matches']:
                        Ganador=partidas['winner_id']
                        Ganador2=str(Ganador)
                        diccequiposT['Empieza']=partidas['begin_at']
                        diccequiposT['Termina']=partidas['end_at']
                        diccequiposT['Tipo']=partidas['match_type']
                        diccequiposT['Enfrentamiento']=partidas['name']
                        diccequiposT['Ganador']=diccequipos[Ganador2]
                        listaequipos.append(diccequiposT.copy())
        return listaequipos
t=requests.get(URL_BASE+'//lives',params=parametros)
datos2=t.json()
def obtener_enfrentamientos_lives():
        dicclol={}
        listalol=[]
        for torneosdirecto in datos2:
                if torneosdirecto['event']['game']=='league-of-legends':
                        dicclol['URLStream']=torneosdirecto['event']['stream_url']
                        dicclol['Juego']=torneosdirecto['event']['game']
                        dicclol['id']=torneosdirecto['event']['id']
                        dicclol['Tid']=torneosdirecto['event']['tournament_id']
                        listalol.append(dicclol.copy())
        return listalol
def obtener_match_lives():
        diccmatch={}
        listamatch=[]
        listaids=[]
        diccenfrentamiento={}
        for identificador in obtener_enfrentamientos_lives():
                listaids.append(identificador['Tid'])
        for ids in listaids:
                for matches in datos2:
                        if matches['match']['tournament']['id']==ids:
                                diccmatch['Termina']=matches['match']['tournament']['end_at']
                                diccmatch['Nombre']=matches['match']['tournament']['slug'].capitalize()
                                diccmatch['NombreMatch']=matches['match']['name']
                                listamatch.append(diccmatch.copy())
        return listamatch
#league-of-legends

