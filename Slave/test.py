import requests
import json
import pickle

server = "http://127.0.0.1:5000/V1.0/"

resp_create = requests.post(server + "createvm", json={
    "name": "VM",
    "cores": 2,
    "memory": 200,
    "storage": 20
})

resp_create = requests.post(server + "createvm", json={
    "name": "othername",
    "cores": 2,
    "memory": 200,
    "storage": 20
})

resp_create = requests.post(server + "createvm", json={
    "name": "name",
    "cores": 2,
    "memory": 200,
    "storage": 20
})

print (resp_create.content)

uuid = resp_create.content.decode()
uuid = json.loads(uuid)
uuid = uuid["data"]["uuid"]

resp_reboot = requests.post(server + "reboot", json={
    "uuid": uuid
})

print (resp_reboot.content)

resp_list = requests.get(server + "list")

print (resp_list.content)