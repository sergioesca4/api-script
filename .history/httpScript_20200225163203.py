import requests
import json
import os
import random
from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN = os.getenv('PROD_ACCESS_TOKEN')
API_BASE = os.getenv('PROD_API_BASE')
token = { 'access_token': ACCESS_TOKEN }

def printJson(string, blob):
  print(string + '\n', json.dumps(blob, indent=4))

def getOsName():
  r = random.random()
  if r>=0.6:
    return "Windwos 2016 DE"
  else
    return "Red Hat Enterprise 7.4"
class SecurityZoneTesting():
  def __init__(self):
    pass

  def run(self):
    self.postInstances()
    print('Done!')

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

  def postInstances(self):
    self.storages = []

    with open('.payload.json') as json_file:
      payload = json.load(json_file)

      for dataStore in ['DS1', 'DS2']:
        payload['name'] = self.resourcePoolName + dataStore
        self.storages.append(self.postToOpaas('storage', payload))

onboarder = SecurityZoneTesting()
onboarder.run()