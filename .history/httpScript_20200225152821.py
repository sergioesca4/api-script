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
    self.getComputePool()
    self.postCluster()
    self.getServerId()
    self.postClusterHost()
    self.getImage()
    self.patchImage()
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

  def getComputePool(self):
    print('GETing /compute-pools')

    response = requests.get(url=API_BASE+'/compute-pools', params=token, verify=False)
    print('Response', response.status_code)
    computePools = json.loads(response.text)

    for computePool in computePools:
      if computePool['location'] == self.site and 'SAPHANA' in computePool['workloadTypes']:
        self.computePool = computePool
        break

    if hasattr(self, 'computePool'):
      printJson('Found computePool', self.computePool)
    else:
      raise Exception('Failed to find computePool')

  def postCluster(self):
    with open('./payloads/cluster.json') as json_file:
      clusterPayload = json.load(json_file)

      clusterPayload['resourcePoolName'] = self.resourcePoolName
      clusterPayload['poolLocation'] = self.site
      clusterPayload['camConnectionName'] = self.site + 'HANA'
      clusterPayload['pod'] = self.pod
      clusterPayload['computePoolId'] = self.computePool['id']
      clusterPayload['storageIds'] = list(map(lambda storage: storage['id'], self.storages))

      self.cluster = self.postToOpaas('clusters', clusterPayload)
      printJson('Created cluster', self.cluster)

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

  def postClusterHost(self):
    with open('./payloads/clusterHost.json') as json_file:
      clusterHostPayload = json.load(json_file)

      clusterHostPayload['hostName'] = self.hostname
      clusterHostPayload['serverId'] = self.server['id']
      clusterHostPayload['clusterId'] = self.cluster['id']
      clusterHostPayload['site'] = self.site

      self.clusterHost = self.postToOpaas('cluster-hosts', clusterHostPayload)

  def getImage(self):
    response = requests.get(API_BASE+'/images', params=token, verify=False)
    images = json.loads(response.text)

    profilesFilter = lambda profile : profile['name'] == self.profile and list(filter(camTemplatesFilter, profile['camTemplates']))
    camTemplatesFilter = lambda camTemplate : 'SAPHANA' in camTemplate['workloadTypes']

    for image in images:
      if 'site' in image.keys() and image['site'] == self.site and list(filter(profilesFilter, image['profiles'])):
        try:
          self.images.append(image)
        except:
          self.images = [image]

    if hasattr(self, 'images'):
      printJson('Found images', self.images)
    else:
      raise Exception('Failed to find image')

  def patchImage(self):
    print('PATCHing /images')

    for image in self.images:
      profile = list(filter(lambda profile : profile['name'] == self.profile, image['profiles']))[0]
      sampleImageInfo = profile['imageInfo'][0]

      imagePatch = [
        {
          "op": "add",
          "path": "/profiles/3x/imageInfo/-",
          "value": {
            "resourcePoolName": self.resourcePoolName,
            "clusterId": self.cluster['id'],
            "osTemplate": sampleImageInfo['osTemplate'],
            "imageUuid": sampleImageInfo['imageUuid'],
            "guestId": sampleImageInfo['guestId']
          }
        }
      ]

      print('PATCHing', imagePatch)

      response = requests.patch(
        url=API_BASE+'/images/'+image['id'],
        json=imagePatch,
        params=token,
        verify=False
      )

      print('Response', response.status_code)

      if response.status_code == 200:
        print('Successful patch!')
      else:
        raise Exception('Something went wrong during PATCH!')

onboarder = ClusterHostOnboarder()
onboarder.run()