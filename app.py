import requests
import os
key=os.environ['keyfort']
headers={'TRN-Api-Key' : key}
URL_BASE="https://api.fortnitetracker.com/v1/profile/"
plataforma=str(input("Dime la plataforma "))
cuenta=str(input("Dime la cuenta "))
r=requests.get(URL_BASE+'%s/%s'%(plataforma,cuenta),headers=headers)
doc = r.json()
print(doc)