#!/usr/bin/python

import sys
import sqlite3, re, os
import vlans


db = 'provision.db'
conn = sqlite3.connect(db)
c = conn.cursor()

p_create=re.compile('^create (\w+) vlan (\d+) vm_name (\S+)')
p_destroy=re.compile('^destroy (\w+)$')
p_add=re.compile('^add (\S+) to (\w+)$')
p_remove=re.compile('^remove (\S+) from (\w+)$')

changed = False


def show_table(table_name, fields_info):
  print "table " + table_name
  print fields_info
  print "----------------------------------------------"
  c.execute("select * from " + table_name)
  for row in c:
    print row
  print ""

def show_all():
  # Shows all the tables
  show_table("nodes","node_id | MAC_addr | manage_ip | available | group_name")
  show_table("groups","group_name | vlan_id | vm_name | state")
  show_table("vlans","vlan_id | available ")
  show_table("vms", "vm_name | available")


def check_available(table_name, val_name, val_id):
  # Checks if the desired value is available for allocation
  c.execute('select available from ' + table_name + ' where ' + val_name + ' = ?', (val_id,))
  if c.fetchone()[0] == 0:
    return 0
  return 1


def create_group(command):
  # Unroll the command into individual values
  group_name, vlan_id, vm_name = p_create.match(command).groups()
  vlan_id = int(vlan_id)
    
  try:
    # Make sure that there isn't already a group with this name
    try:
      # This will fail if group_name doesn't exist
      c.execute('select group_name from groups where group_name = ?', (group_name,))
      c.fetchone()[0]
      # If we get to this point, the group already exists, so fail
      print "Group", group_name, "already exists"
      return False
    except:
      pass
    
    # Make sure that the vlan asked for is available
    if not check_available('vlans', 'vlan_id', vlan_id):
      print "vlan id not available"
      return False
    # Make sure that the vm asked for is available
    if not check_available('vms', 'vm_name', vm_name):
      print "vm not available"
      return False
    
    c.execute('update vlans set available = 0 where vlan_id = ?', (vlan_id,))
    c.execute('update vms set available = 0 where vm_name = ?', (vm_name,))
    c.execute('insert into groups values(?,?,?,":(")', (group_name, vlan_id, vm_name,))
    
    return True
  except:
    print "Creating group failed"
    return False

def remove_group(command):
  # Get the group name from the command
  group_name = p_destroy.match(command).groups()[0]
  
  try:
    # Ensure that group_name is a valid group
    try:
      # This will fail is group_name doesn't exist
      c.execute('select group_name from groups where group_name = ?', (group_name,))
      c.fetchone()
    except:
      print "Group", group_name, "does not exist."
      return False
    
    # Get the vlan_id and vm_name from this group
    c.execute('select vlan_id, vm_name from groups where group_name = ?', (group_name,))
    vlan_id, vm_name = c.fetchone()
    # Release the vlan and vm from the group
    c.execute('update vlans set available = 1 where vlan_id = ?', (vlan_id,))
    c.execute('update vms set available = 1 where vm_name = ?', (vm_name,))
    
    # Get and release the nodes which are assigned to this group
    c.execute('select node_id from nodes where group_name = ?', (group_name,))
    for node in c.fetchall():
      print "Removing node", node
      c.execute('update nodes set available = 1, group_name = ? where node_id = ?', ('none', node[0],))
    
    # Remove the group
    c.execute('delete from groups where group_name = ?', (group_name,))
    
    return True
  except:
    print "Removing group failed."
    return False

def move_node(command, add):
  # Unroll the group name and node we want
  if add:
    node_ids, group_name = p_add.match(command).groups()
  else:
    node_ids, group_name = p_remove.match(command).groups()
    group_name = 'none'
  
  for node_id in node_ids.split(','):
    node_id = int(node_id)
      
    # Make sure that the node asked for is available
    if add and not check_available('nodes', 'node_id', node_id):
      print "node id", node_id, "not available"
      continue
    
    # Add / remove the node from the desired group
    c.execute('update nodes set available=?, group_name=? where node_id=?', (1-add, group_name, node_id,))
  
  return True


def deploy(): 
  # Remove machines to be moved from old vlans
  # Remove vlans to be deleted
  # Create new vlans
  c.execute('select * from groups')
  vlans = ""
  for group in c.fetchall():
    # Make the vlan for this group
    vlan_id = str(group[1])
    vlans.make_remove_vlans(vlan_id, True)
    
    # Get the nodes assigned to this group
    c.execute('select node_id from nodes where group_name=?',(group[0],))
    nodes = ""
    for node in c.fetchall():
      nodes += str(node[0]) + ","
    nodes = nodes[:-1]
    print vlan_id, nodes
    # Add the ports to the vlan
    vlans.edit_ports_on_vlan(nodes, vlan_id, True)
  

def parse_command(command):
  global changed
  if command == "exit":
    if changed and raw_input("Commit changes (y/n):") == 'y':
      deploy()
      conn.commit()
    conn.close()
    exit(0)
  elif command == "show":
    show_all()
  elif command == "deploy":
    deploy()
  elif command == "help":
    print '''\nCommand list
0. init
1. show
2. create <group_name> vlan <vlan_id> vm_name <vm_name>
3. destroy <group_name>
4. add <node_ids> to <group_name>
5. remove <node_ids> from <group_name>
6. deploy
7. exit\n'''
  
  elif p_create.match(command):
    if create_group(command): changed = True
  elif p_destroy.match(command):
    if remove_group(command): changed = True
  
  elif p_add.match(command):
    if move_node(command, True): changed = True
  elif p_remove.match(command):
    if move_node(command, False): changed = True
  else:
    print "Invalid command. Type 'help' for a list of valid commands."

if __name__ == "__main__":
  
  if len(sys.argv) == 1:
    # Run interactively
    while True:
      parse_command(raw_input("spl>"))
  else:
    # Send the command_line request as a string
    parse_command(' '.join(sys.argv[1:]))
