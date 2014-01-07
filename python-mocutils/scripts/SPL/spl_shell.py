import spl_command_pattern
import spl_control
import spl_er

class_name={'group':spl_er.Group,
            'vm':spl_er.VM,
            'network':spl_er.Network,
            'node':spl_er.Node}

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

def add_node(cmd):
    '''
    add one node to a group
    '''
    parts = spl_command_pattern.add.match(cmd)
    node_id = int(parts.group(1))
    group_name = parts.group(2)
    print 'add',node_id,'to',group_name
    spl_control.add_node_to_group(node_id,group_name)

def show_table(cmd):
    parts = spl_command_pattern.show_table.match(cmd)
    table = parts.group(1)
    if table not in class_name:
        print 'no such table'
        print 'available tables are:'
        for key in class_name:
            print key
        return
    spl_control.query_db(class_name[table])

def show_all():
    spl_control.query_db(spl_er.Node)
    spl_control.query_db(spl_er.Port)
    spl_control.query_db(spl_er.Network)
    spl_control.query_db(spl_er.VM)
    spl_control.query_db(spl_er.Switch)
    spl_control.query_db(spl_er.Group)

while True:
    cmd = raw_input('spl>')
    if spl_command_pattern.create_group.match(cmd):
        create_group(cmd)
    elif cmd == 'show all':
        show_all()
    elif spl_command_pattern.destroy_group.match(cmd):
        print 'destroy a group'
    elif spl_command_pattern.show_group.match(cmd):
        print 'show group'
    elif spl_command_pattern.show_free_table.match(cmd):
        print 'free table'
    elif spl_command_pattern.show_table.match(cmd):
        show_table(cmd)
    elif spl_command_pattern.change_vlan.match(cmd):
        print 'ch vlan'
    elif spl_command_pattern.change_head.match(cmd):
        print 'ch head'
    elif spl_command_pattern.add.match(cmd):
        print 'add node'
        add_node(cmd)
    elif cmd == 'exit':
        #Might need check before exit
        print 'Bye for now'
        exit()
    else:
        print 'invalid command'
        print 'usage'
        print spl_command_pattern.help_text
        
