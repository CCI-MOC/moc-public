#!/usr/bin/python

import sys, re
from mocutils import db_controls


def print_help():
  print '''\nCommand list
 show all
 show <specific table>
 show free [specific table]
 show group <group_name>
 create vlan <vlan_id>
 destroy vlan <vlan_id>
 create group <group_name> vlan <vlan_id> head-node <vm_name>
 destroy group <group_name>
 add <node_ids> to <group_name>
 remove <node_ids> from <group_name>
 change <group_name> vlan to <vlan_id>
 change <group_name> head to <vm_name>
 deploy
 exit\n'''


def parse_command(controller, command):
  # Look at help for a full listing of commands
  # These are the regex to match user command
  # Create a group
  p_create_group = re.compile('^create group (\w+) vlan (\d+) head-node (\S+)')
  # Destroy a group
  p_destroy_group = re.compile('^destroy group (\w+)$')

  # Add a machine to a group
  p_add = re.compile('^add (\S+) to (\w+)$')
  # Remove a machine from a group
  p_remove = re.compile('^remove (\S+) from (\w+)$')

  # Create a vlan
  p_create_vlan = re.compile('^create vlan (\d+)')
  # Destroy a vlan
  p_destroy_vlan = re.compile('^destroy vlan (\d+)')

  # Show a specific group
  p_show_group = re.compile('^show group (\w+)')
  # Show the free elements of a table
  p_show_free_table = re.compile('^show free (\w+)')
  # Show a specific table
  p_show_table = re.compile('^show (\w+)')
  
  # Change a group's vlan
  p_change_vlan = re.compile('^change (\w+) vlan to (\d+)')
  # Change a group's vm
  p_change_head = re.compile('^change (\w+) head to (\S+)')

  
  if command   == 'exit':
    print "Warning: exiting without deploying will not save any changes."
    sure = raw_input("Are you sure you would like to exit (Y/n):")
    if sure == 'y' or sure == 'Y' or sure == '':
      exit(0)

  elif command == 'deploy':
    controller.deploy()
  
  elif command == 'help':
    print_help()

  # Various options for showing db information
  elif command == 'show all':
    controller.show_db(False)
  elif command == 'show free':
    controller.show_db(True)
  elif p_show_group.match(command):
    name = p_show_group.match(command).groups()[0]
    controller.show_group(name)
  elif p_show_free_table.match(command):
    name = p_show_free_table.match(command).groups()[0]
    controller.show_db(True, name)
  elif p_show_table.match(command):
    name = p_show_table.match(command).groups()[0]
    controller.show_db(False, name)
  
  # Create / destroy a vlan
  elif p_create_vlan.match(command):
    controller.add_remove_vlan_to_db(p_create_vlan.match(command).groups()[0], True)
  elif p_destroy_vlan.match(command):
    controller.add_remove_vlan_to_db(p_destroy_vlan.match(command).groups()[0], False)

  # Create / destroy a group
  elif p_create_group.match(command):
    name, vlan, head_node = p_create_group.match(command).groups()
    controller.create_group(name, vlan, head_node)
  elif p_destroy_group.match(command):
    name = p_destroy_group.match(command).groups()[0]
    controller.remove_group(name)

  # Add / remove nodes from a group
  elif p_add.match(command):
    node_ids, group_name = p_add.match(command).groups()
    controller.move_nodes_group(node_ids, group_name, True)
  elif p_remove.match(command):
    node_ids, group_name = p_remove.match(command).groups()
    controller.move_nodes_group(node_ids, group_name, False)
  
  # Change the vlan / head node of a group
  elif p_change_vlan.match(command):
    group_name, vlan = p_change_vlan.match(command).groups()
    controller.change_vlan(group_name, vlan)
  elif p_change_head.match(command):
    group_name, vm_name = p_change_head.match(command).groups()
    controller.change_head(group_name, vm_name)

  
  else:
    print "Invalid command. Type 'help' for a list of valid commands."


if __name__ == "__main__":
  if len(sys.argv) == 2:
    db_controller = db_controls.DB_Controller(sys.argv[1])
  else:
    db_controller = db_controls.DB_Controller(raw_input("Enter db name:"))
  
  # Run interactively
  while True:
    parse_command(db_controller, raw_input("spl>"))

