import requests
import json

def create_group(group_name,network_id,vm_name):
    payload = {
        "group_name":group_name,
        "network_id":network_id,
        "vm_name":vm_name
    }
    headers  = {'Content-Type': 'application/json'}
    r = requests.post("http://localhost:5000/groups",data=json.dumps(payload),headers = headers)
def get_group(group_name):
    r = requests.get('http://localhost:5000/groups/%s'%group_name)
    print r.text

def get_group_nodes(group_name):
    r = requests.get('http://localhost:5000/groups/%s/nodes'%group_name)
    print r.text
    


    
    
