import os
import requests
key=os.environ['keypanda']
parametros={'token':key}
URL_BASE='https://api.pandascore.co'
r=requests.get(URL_BASE+'//lol/tournaments/running',params=parametros)
datos=r.json()
diccequipos={}
for torneos in datos:
    for equipos in torneos['teams']:
        print(equipos['name'],equipos['id'])
        id=equipos['id']
        id2=str(id)
        diccequipos[id2]=equipos['name']
    for partidas in torneos['matches']:
        print('Empieza a las:',partidas['begin_at'])
        print('Termina a las:',partidas['end_at'])
        print('Tipo de partido',partidas['match_type'])
        print('Enfrentamiento',partidas['name'])
        Ganador=partidas['winner_id']
        Ganador2=str(Ganador)
        print('Ganador:',diccequipos[Ganador2])

t=requests.get(URL_BASE+'//lives',params=parametros)
datos2=t.json()
for torneosdirecto in datos2:
    for directos in torneosdirecto['match']:
        print(directos['games'])
