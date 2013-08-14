#!/usr/bin/python

import pexpect

import sys
sys.path.insert(0, '/etc/moc')
from mocutils import switch as cfg

def make_remove_vlans(vlan_ids, add, switch_ip=cfg.ip, user=cfg.user, pwd=cfg.pwd):
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
