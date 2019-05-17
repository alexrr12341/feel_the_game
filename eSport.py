import os
import requests
key=os.environ['keypanda']
parametros={'token':key}
URL_BASE='https://api.pandascore.co'
r=requests.get(URL_BASE+'//lol/tournaments/running',params=parametros)
datos=r.json()
diccequipos={}
dicctorneo={}
print(datos)
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
for torneosdirecto in datos2:
    print('Hola')
