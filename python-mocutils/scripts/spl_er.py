from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker,backref
Base=declarative_base()

class Node(Base):
    __tablename__='nodes'

    node_id=Column(Integer,primary_key=True)
    mac_addr=Column(String)
    manage_ip=Column(String)
    available=Column(Boolean)
    group_name=Column(String,ForeignKey('groups.name'))
    port_id=Column(Integer,ForeignKey('ports.port_id'))

    #Many to one mapping to group
    group=relationship("Group",backref=backref('nodes',order_by=node_id))
    #One to one mapping to port
    port=relationship("Port",backref=backref('node',uselist=False))

    def __init__(self,node_id,mac_addr="mac",manage_ip="10.0.0.1",available=True):
        self.node_id=node_id 
        self.mac_addr=mac_addr
        self.manage_ip=manage_ip
        self.available=available
    def __repr__(self):
        return "<Node(%r %r %r %r %r %r)"%(self.node_id,self.mac_addr,self.manage_ip,self.available,self.group,self.port)

"""
One to one mapping between group and vm
One to one mapping between group and vlan
Many to one mapping between node and group
"""

class Group(Base):
    __tablename__='groups'
    name=Column(String,primary_key=True)
    vm_name=Column(String,ForeignKey('vms.name'))
    network_id=Column(Integer,ForeignKey('networks.network_id'))
    
    vm=relationship("VM",backref=backref('group',uselist=False))
    network=relationship("Network",backref=backref('group',uselist=False))
    def __init__(self,name="group1"):
        self.name=name

    def __repr__(self):
        return "<Group(%r %r %r)>"%(self.name,self.vm,self.network)

class VM(Base):
    __tablename__='vms'
    name=Column(String,primary_key=True)
    available=Column(Boolean)

    def __init__(self,name="vm1",available=True):
        self.name="vm1"
        self.available=available
    def __repr__(self):
        return "<VM(%r %r)>"%(self.name,self.available)

class Network(Base):
    __tablename__='networks'
    network_id=Column(Integer,primary_key=True)
    network_technology=Column(String)

    def __init__(self,network_id,network_technology="vlan"):
        self.network_id=network_id
        self.network_technology=network_technology
    def __repr__(self):
        return "Network(%r %r)"%(self.network_id,self.network_technology)


class Vlan(Base):
    __tablename__='vlans'
    vlan_id=Column(Integer,primary_key=True)
    available=Column(Boolean) 
    def __init__(self,vlan_id=100,available=True):
        self.vlan_id=vlan_id
        self.available=available
    def __repr__(self):
        return "Vlan(%r %r)"%(self.vlan_id,self.available)

class Port(Base):
    __tablename__='ports'
    port_id=Column(Integer,primary_key=True)
    switch_id=Column(Integer,ForeignKey('switches.switch_id'))
    port_no=Column(Integer)
    switch=relationship("Switch",backref=backref('ports',order_by=port_id))

    def __init__(self,port_id,switch_id,port_no):
        self.port_id=port_id
        self.port_no=port_no
        self.switch_id=switch_id
    def __repr__(self):
        return "Port(%r %r %r)"%(self.port_id,self.switch_id,self.port_no)


class Switch(Base):
    __tablename__='switches'
    switch_id=Column(Integer,primary_key=True)
    script=Column(String)

    def __init__(self,switch_id,script):
        self.switch_id=switch_id
        self.script=script
    def __repr__(self):
        return "Switch(%r %r)"%(self.switch_id,self.script)


engine=create_engine('sqlite:///spl17.db',echo=True)
Base.metadata.create_all(engine)
Session=sessionmaker(bind=engine)
session=Session()

#Check all nodes in g1 connect to same switch.
#run the script, print the nodes

