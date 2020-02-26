import json
import requests

api_token = 'mytokenhere'
api_url = 'https://opaas.amm.ibmcloud.com/api/v1/instances/'
payload = { "defaultpmpPassword": "Hosting@IBM123",
            "departmentName": "Infra",
            "memory": 4,
            "createci": true,
            "createpmp": true,
            "deployEnvironment": "NONPROD",
            "cdir": "GEI",
            "swap": 2,
            "cpu": 1,
            "storage":[],
            "osName": "Red Hat Enterprise 7.4",
            "poolType": "SystemX",
            "enableDr": false,
            "hostname": "geitstent14",
            "customerHostname": "geitstent14",
            "site": "POK02",
            "sshKey": "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAtmidFx2vOvMiU7ws/8sX4cwjPY/rESIfoP49rpMZYg/Pk0jVsO+Qyfz5E9BCru4S65B0FkwAaM7emu4RwEObxQNx1Bcjo5c3eBEUSahNQT4UdMTxzDAt8uLH93agL2bCisqUddx/YpvRDMAPwhnh53TaCO+BPrXvAaD+Hodt4yOUsRdpjpvFZvaNKYNmRISLjd0JvLsYgUYAOGHa0RdMm6qToJdZLti1cVV0GYocFr/Pl8q+x4parR2It53a+KMOdYZR8BtvPHKp1sZwTddxJSzZ/rjriYpDBuXOnHcHjMD7FmDXBm53dmj+2t0YvPzlNjsVyVbLFdJVktSiVGimnw\u003d\u003d",
            "domain": "mhas.ibm.com",
            "zoneName": "Security Zone ENT14",
            "workloadType": "MANAGED",
            "backupFolder": "NFL-APP",
            "backupPolicyGroup": "BU0",
            "pmpResourceDesc": "SDM-CUSTOM-HOSTNAME",
            "subscriptionId": "SDM-10",
            "serviceLevel": "managed_os",
            "contractNumber": "CNTR0010332"
            }

headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(api_token)}
r = requests.post(api_url, data=json.dumps(payload), headers=headers)
n = 0

while n<5:
  '''change variables in payload'''
  make call
  n++

print r.status_code