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
   # connect_nodes_to_ports()
    session.commit()

def create_group(group_name,vm_name):
    group=Group(group_name)
    if check_available(VM,'name=="%s"'%vm_name):
    #NOT working 
    	group.vm=get_entity_by_cond(VM,'name=="%s"'%vm_name)
        group.vm.available=False
    else:
    	print "error: "+vm_name+" not available"
        return
    print "group.vm=",group.vm
    session.add(group)
    session.commit()
