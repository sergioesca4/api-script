import requests
import json
import os
import random
from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN = os.getenv('PROD_ACCESS_TOKEN')
API_BASE = os.getenv('PROD_API_BASE')
token = { 'access_token': ACCESS_TOKEN }

hostnameCounter = 0

def printJson(string, blob):
  print(string + '\n', json.dumps(blob, indent=4))

def getOsName():
  return "Windows 2016 DE" if random.random()>=0.6 else "Red Hat Enterprise 7.4"

def postToOpaas(self, endpoint, payload):
  printJson(f'POSTing to endpoint /{endpoint}', payload)

  response = requests.post(
    url=API_BASE+'/'+endpoint,
    json=payload,
    params=token,
    verify=False
  )

  responseJson = json.loads(response.text)

  print('Response code', response.status_code)
  printJson('Response body', responseJson)

  if response.status_code == 200 and responseJson['id']:
    return responseJson
  else:
    raise Exception('Something went wrong creating the object!')

def postInstance(zoneName):
global hostnameCounter
  with open('./payload.json') as json_file:
    payload = json.load(json_file)
    hostname = f'securityzonetest{hostnameCounter}'
    hostnameCounter+=1
    payload['osName'] = getOsName()
    payload['zoneName'] = zoneName
    payload['hostname'] = hostname
    payload['customerHostname'] = hostname
    postToOpaas('instances', payload)

zoneNames = ["Security Zone EPU00", "Security Zone EPS00", "Security Zone EPU01", "Security Zone EPU02", "Security Zone EPS01"]
for zoneName in zoneNames:
  postInstance(zoneName)