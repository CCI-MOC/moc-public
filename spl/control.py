from er import *
import spl.config

import os
import os.path
import dell

current_user = ""

def query_db(classname):
    all=session.query(classname).all()
    for some in all:
        print some
    return all

def create_user(user_name,password):
    user = User(user_name,password)
    session.add(user)
    session.commit()

def login_user(user_name):
    global current_user
    current_user = user_name

def check_available(classname,cond):
    """
    classname specifies which kind of objects
    cond is a string like "node_id==2"
    """
    return session.query(classname).filter(cond).first().available

def get_entity_by_cond(classname,cond):
    return session.query(classname).filter(cond).first()

def create_node(node_id):
    node = Node(node_id)
    session.add(node)
    session.commit()

def create_nic(nic_id,mac_addr,name):
    nic = NIC(nic_id,mac_addr,name)
    session.add(nic)
    session.commit()

def add_nic(nic_id,node_id):
    nic = get_entity_by_cond(NIC,'nic_id==%d'%nic_id)
    node = get_entity_by_cond(Node,'node_id==%d'%node_id)
    nic.node = node
    session.commit()

def create_switch(switch_id,script):
    switch = Switch(switch_id, script)
    session.add(switch)
    session.commit()
def create_port(port_id,switch_id,port_no):
    switch = get_entity_by_cond(Switch,'switch_id==%d'%switch_id)
    port = Port(port_id,port_no)
    port.switch = switch
    session.add(port)
    session.commit()
def connect_nic(nic_id, port_id):
    nic  = get_entity_by_cond(NIC,'nic_id==%d'%nic_id)
    port = get_entity_by_cond(Port, 'port_id==%d'%port_id)
    nic.port = port 
    session.commit()
def connect_vlan(vlan_id,group_name,nic_name):
    vlan           = get_entity_by_cond(Vlan,'vlan_id==%d'%vlan_id)
    group          = get_entity_by_cond(Group,'group_name=="%s"'%group_name)
    vlan.nic_name  = nic_name
    vlan.group     = group
    session.commit()


def create_vlan(vlan_id):
    vlan = Vlan(vlan_id)
    session.add(vlan)
    session.commit()

def add_node_to_group(node_id,group_name):
    #ownership check

    node=get_entity_by_cond(Node,'node_id==%d'%node_id)
    group=get_entity_by_cond(Group,'group_name=="%s"'%group_name)

    if group.owner_name!=current_user and current_user!="admin":
        print 'access denied'
        return

    if node.available:
        node.group=group
        node.available=False
    else:
        print "error: node ",node_id," not available"
        return
    session.commit()

def remove_node_from_group(node_id,group_name):
    node = get_entity_by_cond(Node, 'node_id==%d'%node_id)
    group = get_entity_by_cond(Group,'group_name=="%s"'%group_name)

    if group.owner_name!=current_user and current_user!="admin":
        print 'access denied'
        return

    if node.group_name != group_name:
        print 'node',node_id,'not in',group_name
        return
    node.group = None
    node.available = True




def create_group(group_name):
    group=Group(group_name)
    user = get_entity_by_cond(User,'user_name=="%s"'%current_user)
    group.owner = user
    session.add(group)
    session.commit()

def destroy_group(group_name):
    #ownership check
    group = get_entity_by_cond(Group,'group_name=="%s"'%group_name)
    if not group:
        print 'Group does not exist'
        return

    if current_user!="admin" and group_name.owner_name != current_user:
        print 'access denied'
        return

    for node in group.nodes:
        node.available = True
    group.nodes = []
    session.delete(group)
    session.commit()


def check_same_non_empty_list(ls):
    for ele in ls:
        if ele != ls[0]: return False
    return ls[0]

def deploy_group(group_name):
    group = get_entity_by_cond(Group,'group_name=="%s"'%group_name)
    port_list = ""
    for node in group.nodes:
        port_list = port_list + str(node.nics[0].port.port_no)+","
    
    port_list = port_list[0:-1]
    vlan_id = group.vlans[0].vlan_id
    print vlan_id
    print port_list
    
    #dell.make_remove_vlans(str(vlan_id),True)
    #dell.edit_ports_on_vlan("",str(vlan_id),True)
