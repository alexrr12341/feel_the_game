import requests
import os
key=os.environ["keyf"]
header={'TRN-Api-Key':key}
URL_BASE='https://api.fortnitetracker.com/v1/'
def tienda_fortnite():
    t=requests.get(URL_BASE+'store',headers=header)
    datos2=t.json()
    tiendaf={}
    listaf=[]
    for tienda in datos2:
        print('Nombre:',tienda['name'])
        print('Rareza',tienda['rarity'])
        print('vBucks',tienda['vBucks'])
        print('Imagen',tienda['imageUrl'])
        tiendaf['Nombre']=tienda['name'] 
        tiendaf['Rareza']=tienda['rarity']
        tiendaf['VBucks']=tienda['vBucks']
        tiendaf['Imagen']=tienda['imageUrl']
        listaf.append(tiendaf)
    return listaf
def estadisticas_fortnite(plat,jugador):
    r=requests.get(URL_BASE+'profile/%s/%s'%(plat,jugador),headers=header)
    datos=r.json()
    lista=['top1','top10','top25','winRatio','matches','score','kills','kd']
    listasolo=['Solo']
    id=datos['accountId']
    tiendag={}
    tiendasq={}
    tiendadu={}
    tiendaso={}
    tiendaso2={}
    tiendadu2={}
    tiendasq2={}
    tiendag2={}
    for infoSolo in lista:
        tiendaso[datos['stats']['p2'][infoSolo]['label']]=datos['stats']['p2'][infoSolo]['value']
    tiendaso2['Solo']=tiendaso
    for infoDuos in lista:
        tiendadu[datos['stats']['p10'][infoDuos]['label']]=datos['stats']['p10'][infoDuos]['value']
    tiendadu2['Duo']=tiendadu
    for infoSquad in lista:
        tiendasq[datos['stats']['p9'][infoSquad]['label']]=datos['stats']['p9'][infoSquad]['value']
    tiendasq2['Squad']=tiendasq
    for infoGeneral in datos['lifeTimeStats']:
        tiendag[infoGeneral['key']]=infoGeneral['value']
    tiendag2['General']=tiendag
    return tiendag2,tiendasq2,tiendadu2,tiendaso2
#0 = General
#1 = Squad
#2 = Duo
#3 = Solo