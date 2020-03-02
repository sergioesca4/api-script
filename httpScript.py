import requests
import json
import os
import random
from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN = os.getenv('PROD_ACCESS_TOKEN')
API_BASE = os.getenv('PROD_API_BASE')
token = { 'access_token': ACCESS_TOKEN }
headers = { 'service-name': 'XXX'}

def printJson(string, blob):
  print(string + '\n', json.dumps(blob, indent=4))

def post(endpoint, payload):
  global headers
  printJson(f'POSTing to endpoint /{endpoint}', payload)

  response = requests.post(
    url=API_BASE+'/'+endpoint,
    json=payload,
    headers=headers,
    params=token,
    verify=False
  )
  print (response.text)
  responseJson = json.loads(response.text)

  print('Response code', response.status_code)
  printJson('Response body', responseJson)

  if response.status_code == 200 and responseJson['id']:
    return responseJson
  else:
    raise Exception('Something went wrong creating the object!')

def postInstance():
  with open('./payload.json') as json_file:
    payload = json.load(json_file)
    post('instances', payload)

postInstance()