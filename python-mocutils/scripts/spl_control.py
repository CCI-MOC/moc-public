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

def check_available(classname,field,value):
    for some in session.query(classname).filter(field=value).all():
	print some

def create_group(group_name,vm_name,network_id,network_technology):
    group=Group(group_name)
    if check_available(vm_name):
    	group.vm=get_vm_by_name(vm_name)
    else:
    	print "error: "+vm_name+" not available"
	return
    if check_available(network_id):
    	group.network=get_network_by_id(network_id)
    else:
    	print "error: network_id "+network_id+" not available"
	return

    session.add(group)
    session.commit()
