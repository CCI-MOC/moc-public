import requests
import json

ip_addr = 'localhost:5000'
def create_group(group_name,network_id,vm_name):
    payload = {
        "group_name":group_name,
        "network_id":network_id,
        "vm_name":vm_name
    }
    headers  = {'Content-Type': 'application/json'}
    r = requests.post("http://%s/groups"%ip_addr,data=json.dumps(payload),headers = headers)
def get_groups():
    r = requests.get('http://%s/groups'%ip_addr,auth=('linzertorte','101450'))
    print r.text

def get_group(group_name):
    r = requests.get('http://%s/groups/%s'%(ip_addr,group_name))
    print r.text

def get_group_nodes(group_name):
    r = requests.get('http://%s/groups/%s/nodes'%(ip_addr,group_name))
    print r.text

def add_node_to_group(group_name,node_id):
    r = requests.get('http://%s/groups/%s/nodes/add/%d'%(ip_addr,group_name,node_id))
    print r.text

def remove_node_from_group(group_name,node_id):
    r = requests.get('http://%s/groups/%s/nodes/remove/%d'%(ip_addr,group_name,node_id))
    print r.text

def destroy_group(group_name):
    r = requests.delete('http://%s/groups/%s'%(ip_addr,group_name),auth=('linzertorte',101450))
    print r.text







