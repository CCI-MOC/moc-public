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

def create_group(group_name,vm_name,vlan_id):
    group=Group(group_name)
    vm=VM(vm_name)
    vlan=Vlan(vlan_id)
    group.vm=vm
    group.vlan=vlan
    session.add(group)
    session.commit()
