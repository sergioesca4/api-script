import json
import requests

api_token = 'mytokenhere'
api_url = 'https://opaas.amm.ibmcloud.com/api/v1/instances/'

headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(api_token)}