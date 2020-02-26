import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN = os.getenv('PROD_ACCESS_TOKEN')
API_BASE = os.getenv('PROD_API_BASE')
token = { 'access_token': ACCESS_TOKEN }

def printJson(string, blob):
  print(string + '\n', json.dumps(blob, indent=4))

class ClusterHostOnboarder():
  def __init__(self):
    pass

  def run(self):
    self.getInputParams()
    self.postStorages()
    self.getServerId()
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

  def getInputParams(self):
    self.profile = input('Enter profile: ')
    self.pod = input('Enter pod: ')
    self.site = input('Enter site (uppercase): ')
    self.resourcePoolName = input('Enter resourcePoolName: ')
    self.hostname = input('Enter hostname: ')

  def postStorages(self):
    self.storages = []

    with open('.payload.json') as json_file:
      payload = json.load(json_file)

      for dataStore in ['DS1', 'DS2']:
        payload['name'] = self.resourcePoolName + dataStore
        self.storages.append(self.postToOpaas('storage', payload))

  def getServerId(self):
    urls = [os.getenv('SERVER_ID_URL_1'), os.getenv('SERVER_ID_URL_2')]

    for url in urls:
      response = requests.get(url)
      servers = json.loads(response.text)
      server = list(filter(lambda server : server['fullyQualifiedDomainName'] == self.hostname, servers))

      if server:
        self.server = server[0]
        break

    if hasattr(self, 'server'):
      printJson('Found server', self.server)
    else:
      raise Exception('Something went wrong finding the server!')

onboarder = ClusterHostOnboarder()
onboarder.run()