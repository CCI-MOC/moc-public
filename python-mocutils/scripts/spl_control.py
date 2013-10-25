from spl_er import *

"""
string,string,integer
"""

def init_db():
    keys=['node_id','mac_addr','manage_ip']

    for line in open('nodes.txt'):
        values=line.rstrip().split(' ')
        d=dict(zip(keys,values))
        session.add(Node(int(d['node_id']),d['mac_addr'],d['manage_ip']))
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
    return session.query(classname).filter(cond).first().available

def get_entity_by_cond(classname,cond):
    return session.query(classname).filter(cond).first()

def create_node_pool():
    c1=Node(1,"mac1","10.0.0.1")
    c2=Node(2,"mac2","10.0.0.2")
    c3=Node(3,"mac3","10.0.0.3")
    c4=Node(4,"mac4","10.0.0.4")
    c5=Node(5,"mac5","10.0.0.5")
    c6=Node(6,"mac6","10.0.0.6")
    session.add(c1)
    session.add(c2)
    session.add(c3)
    session.add(c4)
    session.add(c5)
    session.add(c6)

def create_network_pool():
    net1=Network(101,"vlan")
    net2=Network(102,"vlan")
    session.add(net1)
    session.add(net2)

def create_vm_pool():
    vm1=VM("vm1")
    vm2=VM("vm2")
    session.add(vm1)
    session.add(vm2)

def create_switch_pool():
    sw1=Switch(1,"cisco_snmp.py")
    sw2=Switch(2,"tp_link.py")
    session.add(sw1)
    session.add(sw2)

def create_port_pool():
    p1=Port(201,1,1)
    p2=Port(202,1,2)
    p3=Port(203,1,3)
    p4=Port(204,2,1)
    p5=Port(205,2,2)
    p6=Port(206,2,3)
    session.add(p1)
    session.add(p2)
    session.add(p3)
    session.add(p4)
    session.add(p5)
    session.add(p6)
def connect_nodes_to_ports():
    c1=get_entity_by_cond(Node,'node_id==1')
    c2=get_entity_by_cond(Node,'node_id==2')
    c3=get_entity_by_cond(Node,'node_id==3')
    c4=get_entity_by_cond(Node,'node_id==4')
    c5=get_entity_by_cond(Node,'node_id==5')
    c6=get_entity_by_cond(Node,'node_id==6')

    p1=get_entity_by_cond(Port,'port_id==201')
    p2=get_entity_by_cond(Port,'port_id==202')
    p3=get_entity_by_cond(Port,'port_id==203')
    p4=get_entity_by_cond(Port,'port_id==204')
    p5=get_entity_by_cond(Port,'port_id==205')
    p6=get_entity_by_cond(Port,'port_id==206')
    c1.port=p1
    c2.port=p2
    c3.port=p3
    c4.port=p4
    c5.port=p5
    c6.port=p6

def load_resources():
    create_node_pool()
    create_network_pool()
    create_vm_pool()
    create_switch_pool()
    create_port_pool()
    connect_nodes_to_ports()
    session.commit()

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
    group=get_entity_by_cond(Group,'group_name=="%s"'%group_name)
    nodes=session.query(Node).filter('group_name=="%s"'%group_name)
    for node in nodes:
	print "%s %s"%(node.mac_addr,node.manage_ip)
    print group.network_id
    switches=[]
    for node in nodes:
	switches.append(node.port.switch_id)
    #Check all the nodes in the group are connected to the same switch 
    switch_id=check_same_non_empty_list(switches)
    if switch_id==False:
	print "error: ports not in same switch"
        return
    print "same switch ",switch_id
    switch=get_entity_by_cond(Switch,'switch_id==%d'%switch_id)
    print switch.script
    group.deployed = True
	
