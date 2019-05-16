import requests
import os
plat=str(input("¿Cual es tu plataforma? (pc,xbl,psn) "))
jugador=str(input("¿Cual es el nombre de jugador? "))
key=os.environ["keyf"]
header={'TRN-Api-Key':key}
URL_BASE='https://api.fortnitetracker.com/v1/'
r=requests.get(URL_BASE+'profile/%s/%s'%(plat,jugador),headers=header)
try:
    datos=r.json()
    lista=['top1','top10','top25','winRatio','matches','score','kills','kd']
    print('Plataforma:',datos['platformNameLong'])
    print('Informacion de Solo')
    id=datos['accountId']
    for infoSolo in lista:
        print(datos["stats"]["p2"][infoSolo]["label"],':',datos["stats"]["p2"][infoSolo]["value"])
    print('Informacion de Duo')
    for infoDuos in lista:
        print(datos["stats"]["p10"][infoDuos]["label"],':',datos["stats"]["p10"][infoDuos]["value"])
    print('Informacion de Squad')
    for infoSquad in lista:
        print(datos["stats"]["p9"][infoSquad]["label"],':',datos["stats"]["p9"][infoSquad]["value"])
    print('Informacion General')
    for infoGeneral in datos['lifeTimeStats']:
        print(infoGeneral['key'],':',infoGeneral['value'])
    URL_Historial='https://api.fortnitetracker.com'+'/v1/store'
    t=requests.get(URL_Historial,headers=header)
    datos2=t.json()
    for tienda in datos2:
        print('Nombre:',tienda['name'])
        print('Rareza',tienda['rarity'])
        print('vBucks',tienda['vBucks'])
        print('Imagen',tienda['imageUrl'])
except:
    print('Ese usuario no existe')
    