import spl_command_pattern
import spl_control
import spl_er

def create_group(cmd):
    '''
    do the neccessary parsing
    and call spl_control
    '''
    parts = spl_command_pattern.create_group.match(cmd)
    group_name = parts.group(1)
    network_id = int(parts.group(2))
    vm_name = parts.group(3)
    print group_name, network_id, vm_name
    spl_control.create_group(group_name,vm_name,network_id)


while True:
    cmd = raw_input('spl>')
    if spl_command_pattern.create_group.match(cmd):
        create_group(cmd)
    elif spl_command_pattern.destroy_group.match(cmd):
        print 'destroy a group'
    elif spl_command_pattern.show_group.match(cmd):
        print 'show group'
    elif spl_command_pattern.show_free_table.match(cmd):
        print 'free table'
    elif spl_command_pattern.show_table.match(cmd):
        print 'table'
    elif spl_command_pattern.change_vlan.match(cmd):
        print 'ch vlan'
    elif spl_command_pattern.change_head.match(cmd):
        print 'ch head'
