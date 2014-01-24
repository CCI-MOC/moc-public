from spl.er import *
import spl.config
import spl.control
def create_node_pool():
    keys=['node_id','mac_addr','manage_ip']

    for line in open(spl.config.file_names["node"]):
        values=line.rstrip().split(' ')
        d=dict(zip(keys,values))
        session.add(Node(int(d['node_id']),d['mac_addr'],d['manage_ip']))
    session.commit()

def create_network_pool():
    keys=['network_id','network_technology']

    for line in open(spl.config.file_names["network"]):
        values=line.rstrip().split(" ")
        d=dict(zip(keys,values))
        session.add(Network(int(d["network_id"]),d["network_technology"]))
    session.commit()

def create_vm_pool():
    keys=['vm_name']
    for line in open(spl.config.file_names["vm"]):
        values = line.rstrip().split(" ")
        d = dict(zip(keys,values))
        session.add(VM(d["vm_name"]))
    session.commit()


def create_switch_pool():
    keys=["switch_id","script"]
    for line in open(spl.config.file_names["switch"]):
        values = line.rstrip().split(" ")
        d = dict(zip(keys,values))
        session.add(Switch(int(d["switch_id"]),d["script"]))
    session.commit()

def create_port_pool():
    keys=["port_id","switch_id","port_no"]
    for line in open(spl.config.file_names["port"]):
        values = line.rstrip().split(" ")
        d = dict(zip(keys,values))
        session.add(Port(int(d["port_id"]),int(d["switch_id"]),int(d["port_no"])))
    session.commit()

def connect_node_to_port():

    keys=["node_id","port_id"]
    for line in open(spl.config.file_names["connect"]):
        values = line.rstrip().split(" ")
        d=dict(zip(keys,values))
        node=spl.control.get_entity_by_cond(Node,"node_id==%d"%int(d["node_id"]))
        port=spl.control.get_entity_by_cond(Port,"port_id==%d"%int(d["port_id"]))
        node.port=port
    session.commit()

def add_users():
    keys=["user_name","password","user_type"]
    for line in open(spl.config.file_names["user"]):
        values = line.rstrip().split(" ")
        d = dict(zip(keys,values))
        session.add(User(d["user_name"],d["password"],d["user_type"]))
    session.commit()

def load_resources():
    create_node_pool()
    create_network_pool()
    create_vm_pool()
    create_switch_pool()
    create_port_pool()
    connect_node_to_port()
    add_users()

if __name__=='__main__':
    load_resources()
