import requests
import os
from flask import abort
key=os.environ["keyf"]
header={'TRN-Api-Key':key}
URL_BASE='https://api.fortnitetracker.com/v1/'
def tienda_fortnite():
    t=requests.get(URL_BASE+'store',headers=header)
    datos2=t.json()
    if t.status_code==200:
        tiendaf={}
        listaf=[]
        for tienda in datos2:
            if tienda['storeCategory']=='BRWeeklyStorefront':
                tiendaf['Nombre']=tienda['name'] 
                tiendaf['Rareza']=tienda['rarity']
                tiendaf['VBucks']=tienda['vBucks']
                tiendaf['Tipo']=tienda['storeCategory']
                tiendaf['Imagen']=tienda['imageUrl']
                listaf.append(tiendaf.copy())
        return listaf
    else:
        abort(404)
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
    if r.status_code==200:
        for infoSolo in lista:
            tiendaso[datos['stats']['p2'][infoSolo]['label']]=datos['stats']['p2'][infoSolo]['value']
        for infoDuos in lista:
            tiendadu[datos['stats']['p10'][infoDuos]['label']]=datos['stats']['p10'][infoDuos]['value']
        for infoSquad in lista:
            tiendasq[datos['stats']['p9'][infoSquad]['label']]=datos['stats']['p9'][infoSquad]['value']
        for infoGeneral in datos['lifeTimeStats']:
            tiendag[infoGeneral['key']]=infoGeneral['value']
        return tiendag,tiendasq,tiendadu,tiendaso
    else:
        abort(404)
#0 = General
#1 = Squad
#2 = Duo
#3 = Solo