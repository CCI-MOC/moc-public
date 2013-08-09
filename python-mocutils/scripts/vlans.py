#!/usr/bin/python

import sys
sys.path.insert(0, '/etc/moc')
from mocutils import switch as cfg

import pexpect

def make_remove_vlans(vlan_ids, add, switch_ip='192.168.0.1', user=cfg.user, pwd=cfg.pwd):
  # Expects that you send a string which is a comma separated list of vlan_ids and a bool for adding or removing
  
  p = pexpect.spawn('telnet ' + switch_ip)
  p.logfile = sys.stdout
  p.expect('User:')
  p.sendline(user + '\r')
  p.expect('Password:')
  p.sendline(pwd + '\r')
  p.expect('TP-LINK')
  p.sendline('enable\r')
  p.expect('TP-LINK')
  p.sendline('configure\r')
  p.expect('TP-LINK')
  p.sendline('vlan database\r')
  p.expect('TP-LINK')
  
  for vlan_id in vlan_ids.split(','):
    if add:
      p.sendline('vlan '+ vlan_id + '\r')
    else:
      p.sendline('no vlan '+ vlan_id + '\r')
    p.expect('TP-LINK')
  
  p.sendline('exit\r')
  p.expect('TP-LINK')
  p.sendline('exit\r')
  p.expect('TP-LINK')
  p.sendline('exit\r')
  p.expect('TP-LINK')
  p.sendline('exit\r')
  p.expect('foreign host')

def edit_ports_on_vlan(port_ids, vlan_id, add, switch_ip='192.168.0.1', user=cfg.user, pwd=cfg.pwd):
  # Expects that you send a comma separated list of ports
  # A string for vlan_id
  # And a bool for adding (True = adding, False = Removing)
  
  p=pexpect.spawn('telnet ' + switch_ip)
  p.logfile = sys.stdout
  p.expect('User:')
  p.sendline(user + '\r')
  
  p.expect('Password:')
  p.sendline(pwd + '\r')
  
  p.expect('TP-LINK')
  p.sendline('enable\r')
  
  p.expect('TP-LINK')
  p.sendline('configure\r')
  
  p.expect('TP-LINK')
  for port_id in port_ids.split(','):
    p.sendline('interface ethernet ' + port_id + '\r')
    p.expect('TP-LINK')
    
    if add:
      p.sendline('switchport allowed vlan add ' + vlan_id + '\r')
    else:
      p.sendline('switchport allowed vlan remove ' + vlan_id + '\r')
    p.expect('TP-LINK')
  
  p.sendline('exit\r')
  p.expect('TP-LINK')
  p.sendline('exit\r')
  p.expect('TP-LINK')
  p.sendline('exit\r')
  p.expect('TP-LINK')
  p.sendline('exit\r')
  p.expect('foreign host')
