from er import *
import spl.config

import os
import os.path

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

    


def create_group(group_name,vm_name,network_id):
    #str,str,int

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
        spl.config.paths['headnode-config'],
        str(group.network_id),
        'machines.txt',
    )
  
    machines_dirname = os.path.dirname(machines_filename) 
    if not os.path.isdir(machines_dirname):
        os.mkdir(machines_dirname) 
      
    with open(machines_filename, 'w') as f:
        for node in nodes:
            f.write(("%s %s\n"%(node.mac_addr,node.manage_ip)))


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

    switch=get_entity_by_cond(Switch,'switch_id==%d'%switch_id)

    import cisco_snmp
    switch_drivers = {'cisco_snmp.py':cisco_snmp}
    driver = switch_drivers[switch.script]

        
    
    
    print group.network_id
    driver.make_remove_vlans(str(group.network_id),True)
    print 'ports'+ports
    driver.edit_ports_on_vlan(ports,str(group.network_id),True)

    os.system(('../vm-vlan up %s %s' % (group.network_id,group.vm_name))) 
  
    group.deployed = True
    
