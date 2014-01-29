import re

help_text='''
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
exit
'''
create_user = re.compile('^create user (\w+) (\w+)$')

create_group = re.compile('^create group (\w+) vlan (\d+) head-node (\S+)')
destroy_group = re.compile('^destroy group (\w+)$')

add = re.compile('^add (\S+) to (\w+)$')
# Remove a machine from a group
remove = re.compile('^remove (\S+) from (\w+)$')

# Create a vlan
create_vlan = re.compile('^create vlan (\d+)')
# Destroy a vlan
destroy_vlan = re.compile('^destroy vlan (\d+)')

# Show a specific group
show_group = re.compile('^show group (\w+)')
# Show the free elements of a table
show_free_table = re.compile('^show free (\w+)')
# Show a specific table
show_table = re.compile('^show (\w+)')


# Change a group's vlan
change_vlan = re.compile('^change (\w+) vlan to (\d+)')
# Change a group's vm
change_head = re.compile('^change (\w+) head to (\S+)')

#create a node
create_node = re.compile('^node create (\d+)$')
#create a nic
create_nic = re.compile('^nic create (\d+) (\w+) (\w+)$')
#add a nic to node
add_nic = re.compile('^nic add (\d+) (\d+)$')

#connect a nic to port, nic_id, port_id
connect_nic = re.compile('^nic connect (\d+) (\d+)$')

#create a switch
create_switch = re.compile('^switch create (\d+) (\w+)$')
#create a port , port_id, switch_id, port_no
create_port = re.compile('^port create (\d+) (\d+) (\d+)$')
