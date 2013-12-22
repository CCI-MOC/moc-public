from spl_er import *
import spl_config

import os
import os.path

"""
string,string,integer
"""

def create_node_pool():
    keys=['node_id','mac_addr','manage_ip']

    for line in open(spl_config.file_names["node"]):
        values=line.rstrip().split(' ')
        d=dict(zip(keys,values))
        session.add(Node(int(d['node_id']),d['mac_addr'],d['manage_ip']))
    session.commit()

def create_network_pool():
    keys=['network_id','network_technology']
    
    for line in open(spl_config.file_names["network"]):
        values=line.rstrip().split(" ")
        d=dict(zip(keys,values))
        session.add(Network(int(d["network_id"]),d["network_technology"]))
    session.commit()

def create_vm_pool():
    keys=['vm_name']
    for line in open(spl_config.file_names["vm"]):
        values = line.rstrip().split(" ")
        d = dict(zip(keys,values))
        session.add(VM(d["vm_name"]))
    session.commit()


def create_switch_pool():
    keys=["switch_id","script"]
    for line in open(spl_config.file_names["switch"]):
        values = line.rstrip().split(" ")
        d = dict(zip(keys,values))
        session.add(Switch(int(d["switch_id"]),d["script"]))
    session.commit()

def create_port_pool():
    keys=["port_id","switch_id","port_no"]
    for line in open(spl_config.file_names["port"]):
        values = line.rstrip().split(" ")
        d = dict(zip(keys,values))
        session.add(Port(int(d["port_id"]),int(d["switch_id"]),int(d["port_no"])))
    session.commit()

def query_db(classname):
    all=session.query(classname).all()
    for some in all:
        print some

def check_available(classname,cond):
    """
    classname specifies which kind of objects
    cond is a string like "node_id==2"
    """
    print classname, cond
    return session.query(classname).filter(cond).first().available

def get_entity_by_cond(classname,cond):
    return session.query(classname).filter(cond).first()

def connect_node_to_port():

    keys=["node_id","port_id"]
    for line in open(spl_config.file_names["connect"]):
        values = line.rstrip().split(" ")
        d=dict(zip(keys,values))
        node=get_entity_by_cond(Node,"node_id==%d"%int(d["node_id"]))
        port=get_entity_by_cond(Port,"port_id==%d"%int(d["port_id"]))
        node.port=port
    session.commit()
    
def load_resources():
    create_node_pool()
    create_network_pool()
    create_vm_pool()
    create_switch_pool()
    create_port_pool()
    connect_node_to_port()
    

def add_node_to_group(node_id,group_name):
    node=get_entity_by_cond(Node,'node_id==%d'%node_id)
    group=get_entity_by_cond(Group,'group_name=="%s"'%group_name)

    if node.available:
        node.group=group
        node.available=False
    else:
        print "error: node ",node_id," not available"
    session.commit()


def create_group(group_name,vm_name,network_id):
    #str,str,int
    print "create a group"
    group=Group(group_name)
    vm_name_cond='vm_name=="%s"'%vm_name
    network_id_cond='network_id==%d'%network_id
    if check_available(VM,vm_name_cond):
        group.vm=get_entity_by_cond(VM,vm_name_cond)
        group.vm.available=False
    else:
        print "error: vm "+vm_name+" not available"
        return
    
    if check_available(Network,network_id_cond):
        group.network=get_entity_by_cond(Network,network_id_cond)
        group.network.available=False
    else:
        print "error: network "+network_id+" not available"
        return
    session.add(group)
    session.commit()

def check_same_non_empty_list(ls):
    for ele in ls:
        if ele != ls[0]: return False
    return ls[0]

def deploy_group(group_name):
    """Deploys the group named `group_name`

    This does the following:

    1. Set up the vlan associated with the group
    2. Connect the head node vm to the vlan
    3. Supply the necessary machine information to the head node via virtio
       filesystem.
    """
    group=get_entity_by_cond(Group,'group_name=="%s"'%group_name)
    nodes=session.query(Node).filter('group_name=="%s"'%group_name)
    
    
    machines_filename = os.path.join(
        spl_config.paths['headnode-config'],
        str(group.network_id),
        'machines.txt',
    )
  
    machines_dirname = os.path.dirname(machines_filename) 
    if not os.path.isdir(machines_dirname):
        os.mkdir(machines_dirname) 
    
    with open(machines_filename, 'w') as f:
        for node in nodes:
            f.write(("%s %s\n"%(node.mac_addr,node.manage_ip)))
    print group.network_id
    switches=[]
    ports='';
    for node in nodes:
        switches.append(node.port.switch_id)
        ports+=str(node.port.port_no)+','
    #Check all the nodes in the group are connected to the same switch 
    switch_id=check_same_non_empty_list(switches)
    if switch_id==False:
        # TODO: raise an exception
        print "error: ports not in same switch"
        return
    print "same switch ",switch_id
#    switch=get_entity_by_cond(Switch,'switch_id==%d'%switch_id)
#    print switch.script
#    TODO: factor this out so we can get the switch type from the database
    import cisco_snmp as switch
    print group.network_id
    switch.make_remove_vlans(str(group.network_id),True)
    print 'ports'+ports
    switch.edit_ports_on_vlan(ports,str(group.network_id),True)
    
    os.system(('../vm-vlan up %s %s' % (group.network_id,group.vm_name))) 

    group.deployed = True
    
