#!/usr/bin/python

import sys
sys.path.insert(0, '/etc/moc')
from mocutils import switch as cfg

import pexpect

def edit_ports_on_vlan(ports, vlan_id, add, switch_ip='192.168.0.1', user=cfg.user, pwd=cfg.pwd):
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
  for port in ports.split(','):
    p.sendline('interface ethernet ' + port + '\r')
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
