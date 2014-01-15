import requests
import json
payload = {
    "group_name":"group2",
    "network_id":102,
    "vm_name":"vm2",
}
headers = {'Content-Type': 'application/json'}

r = requests.post('http://localhost:5000/groups',data=json.dumps(payload),headers=headers)
r = requests.get('http://localhost:5000/groups')
print r.text

