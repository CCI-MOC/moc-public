#!/usr/bin/python

import sqlite3

def _create_tables(c):
  c.execute('''CREATE TABLE nodes
        (node_id integer primary key, mac_addr string, manage_ip string, available integer, group_name string)''')

  c.execute('''CREATE TABLE groups
        (group_name string primary key, vlan_id integer,head_node string,state string)''')

  c.execute('''CREATE TABLE vlans
        (vlan_id integer primary key, available integer)''')

  c.execute('''CREATE TABLE vms
        (vm_name string primary key, available integer)''')

def _add_nodes(c, mac_ip_list):
  node_id=1
  for line in open(mac_ip_list, 'r'):
    line = line.rstrip()
    mac, ip_byte = line.split(' ')
    c.execute('''INSERT INTO nodes
        values(?,?,?,1,'none')''', (node_id, mac, '10.0.0.' + ip_byte,))
    node_id += 1

def _add_vlans(c, vlan_list):
  # This assumes that you're passing the vlans as an integer list
  # If want to give file, will have to parse before
  for vlan in vlan_list:
    c.execute('''INSERT INTO vlans
        values(?,1)''',(vlan,))

def _add_vms(c, vm_list):
  # This assumes passing a file of vm_s
  for vm in open(vm_list, 'r'):
    vm = vm.rstrip()
    c.execute('''INSERT INTO vms
        values(?,1)''', (vm,))

def db_setup(mac_ip_list, vlan_list, vm_list, db='provision.db'):
  conn = sqlite3.connect(db)
  c = conn.cursor()

  # Create the tables
  _create_tables(c)

  # Add addresses (mac and ip) to the tables
  # Addresses should be specifed in a file passed in mac_ip_list
  _add_nodes(c, mac_ip_list)

  # Vlans should be passed in as a list
  # If a file is desired, that will have to be parsed before
  _add_vlans(c, vlan_list)

  # Vms should be passed as a file
  _add_vms(c, vm_list)

  conn.commit()
  conn.close()


if __name__ == "__main__":
  import sys

  if len(sys.argv) != 4:
    print "Incorrect usage. Should be '" + sys.argv[0] + "<address file> <vlan_list> <vm_list_file>"
    exit(1)

  mac_ip_list, vlan_list, vm_list = sys.argv[1:]
  vlan_list = vlan_list.split(',')

  vlan_real_list = []
  for vlan in vlan_list:
    if '-' not in vlan:
      vlan_real_list.append(int(vlan))
    else:
      parts = vlan.split('-')
      vlan_real_list.extend(range(int(parts[0]), int(parts[1])+1))

  db_setup(mac_ip_list, vlan_real_list, vm_list)
  
