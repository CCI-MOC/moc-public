from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker,backref
Base=declarative_base()

class Node(Base):
    __tablename__='nodes'

    node_id=Column(Integer,primary_key=True)
    mac_addr=Column(String)
    manage_ip=Column(String)
    available=Column(Boolean)

    #many to one mapping to group
    group_name=Column(String,ForeignKey('groups.name'))
    group=relationship("Group",backref=backref('nodes',order_by=node_id))

    def __init__(self,node_id,mac_addr="mac",manage_ip="10.0.0.1",available=True):
        self.node_id=node_id 
        self.mac_addr=mac_addr
        self.manage_ip=manage_ip
        self.available=available
    def __repr__(self):
        return "<Node(%r %r %r %r %r)"%(self.node_id,self.mac_addr,self.manage_ip,self.available,self.group)

class Group(Base):
    __tablename__='groups'
    name=Column(String,primary_key=True)
    vm_name=Column(String,ForeignKey('vms.name'))
    vlan_id=Column(Integer,ForeignKey('vlans.vlan_id'))
    vm=relationship("VM")
    vlan=relationship("Vlan")
    def __init__(self,name="group1"):
        self.name=name

    def __repr__(self):
        return "<Group(%r)>"%(self.name)

class VM(Base):
    __tablename__='vms'
    name=Column(String,primary_key=True)
    available=Column(Boolean)

    def __init__(self,name="vm1",available=True):
        self.name="vm1"
        self.available=available
    def __repr__(self):
        return "<VM( %r %r)>"%(self.name,self.available)

class Vlan(Base):
    __tablename__='vlans'
    vlan_id=Column(Integer,primary_key=True)
    available=Column(Boolean) 
    def __init__(self,vlan_id=100,available=True):
        self.vlan_id=vlan_id
        self.available=available
    def __repr__(self):
        return "Vlan(%r %r)"%(self.vlan_id,self.available)


engine=create_engine('sqlite:///spl6.db',echo=True)
Base.metadata.create_all(engine)
Session=sessionmaker(bind=engine)
session=Session()
c1=Node(1,"mac1","10.0.0.1")
c2=Node(2,"mac2","10.0.0.2")
c3=Node(3,"mac3","10.0.0.3")
c4=Node(4,"mac4","10.0.0.4")
c5=Node(5,"mac4","10.0.0.5")
g1=Group("group1")
vm1=VM("vm1")
vlan1=Vlan(109)
g1.nodes=[c2,c4]
session.add(g1)
session.commit()
