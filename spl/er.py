from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker,backref
Base=declarative_base()

class Node(Base):
    __tablename__='nodes'

    node_id    = Column(Integer,primary_key=True)
    mac_addr   = Column(String)
    manage_ip  = Column(String)
    available  = Column(Boolean)
    group_name = Column(String,ForeignKey('groups.group_name'))
    port_id    = Column(Integer,ForeignKey('ports.port_id'))
    #Many to one mapping to group
    group      = relationship("Group",backref=backref('nodes',order_by=node_id))
    #One to one mapping to port
    port       = relationship("Port",backref=backref('node',uselist=False))
    
    def __init__(self,node_id,mac_addr = "mac",manage_ip = "10.0.0.1",available = True):
        self.node_id   = node_id 
        self.mac_addr  = mac_addr
        self.manage_ip = manage_ip
        self.available = available

    def __repr__(self):
        return "<Node(%r %r %r %r %r %r)"%(
                self.node_id,
                self.mac_addr,
                self.manage_ip,
                self.available,
                self.group.group_name if self.group else None,
                self.port)

"""
One to one mapping between group and vm
One to one mapping between group and vlan
Many to one mapping between node and group
"""

class Group(Base):
    __tablename__='groups'
    group_name  = Column(String,primary_key=True)
    vm_name     = Column(String,ForeignKey('vms.vm_name'))
    network_id  = Column(Integer,ForeignKey('networks.network_id'))
    deployed    = Column(Boolean)
    owner_name  = Column(String,ForeignKey('users.user_name'))
    
    vm          = relationship("VM",backref=backref('group',uselist=False))
    network     = relationship("Network",backref=backref('group',uselist=False))
    
    #Many to one mapping to User
    owner       = relationship("User",backref=backref('groups',order_by=group_name))

    def __init__(self,group_name):
        self.group_name = group_name
        self.deployed   = False

    def __repr__(self):
      return "<Group(%r %r %r %r %r)>"%(
              self.group_name,
              self.vm,
              self.network,
              self.deployed,
              self.owner_name)

class VM(Base):
    __tablename__ = 'vms'
    vm_name       = Column(String,primary_key=True)
    available     = Column(Boolean)

    def __init__(self,vm_name,available=True):
        self.vm_name   = vm_name
        self.available = available

    def __repr__(self):
        return "<VM(%r %r)>"%(self.vm_name,self.available)

class Network(Base):
    __tablename__      = 'networks'
    network_id         = Column(Integer,primary_key=True)
    network_technology = Column(String)
    available          = Column(Boolean)

    def __init__(self,network_id,network_technology="vlan",available=True):
        self.network_id         = network_id
        self.network_technology = network_technology
	self.available          = available
    def __repr__(self):
        return "Network(%r %r %r)"%(
                self.network_id,
                self.network_technology,
                self.available)


class Vlan(Base):
    __tablename__ ='vlans'
    vlan_id       = Column(Integer,primary_key=True)
    available     = Column(Boolean) 

    def __init__(self,vlan_id,available=True):
        self.vlan_id   = vlan_id
        self.available = available
    def __repr__(self):
        return "Vlan(%r %r)"%(self.vlan_id,self.available)

class Port(Base):
    __tablename__ = 'ports'
    port_id       = Column(Integer,primary_key=True)
    switch_id     = Column(Integer,ForeignKey('switches.switch_id'))
    port_no       = Column(Integer)
    switch        = relationship("Switch",backref=backref('ports',order_by=port_id))

    def __init__(self,port_id,switch_id,port_no):
        self.port_id   = port_id
        self.port_no   = port_no
        self.switch_id = switch_id
    def __repr__(self):
        return "Port(%r %r %r)"%(self.port_id,self.switch_id,self.port_no)


class Switch(Base):
    __tablename__ = 'switches'
    switch_id     = Column(Integer,primary_key=True)
    script        = Column(String)

    def __init__(self,switch_id,script):
        self.switch_id = switch_id
        self.script    = script
    def __repr__(self):
        return "Switch(%r %r)"%(self.switch_id,self.script)

class User(Base):
    __tablename__ = 'users'
    user_name = Column(String,primary_key=True)
    user_type = Column(String)
    password  = Column(String)

    def __init__(self,user_name,password,user_type="plain"):
        self.user_name = user_name
        self.user_type = user_type
        self.password  = password
    def __repr__(self):
        return "User<%r %r %r>"%(self.user_name,self.user_type,self.password)

engine=create_engine('sqlite:///spl.db',echo=False)
Base.metadata.create_all(engine)
Session=sessionmaker(bind=engine)
session=Session()

#Check all nodes in g1 connect to same switch.
#run the script, print the nodes

