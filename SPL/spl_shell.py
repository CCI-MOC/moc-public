import spl.command_pattern
import spl.control
import spl.er

class_name={'group':spl.er.Group,
            'vm':spl.er.VM,
            'network':spl.er.Network,
            'node':spl.er.Node,
            'user':spl.er.User}

def create_group(cmd):
    '''
    do the neccessary parsing
    and call spl.control
    '''
    parts = spl.command_pattern.create_group.match(cmd)
    group_name = parts.group(1)
    network_id = int(parts.group(2))
    vm_name = parts.group(3)
    print group_name, network_id, vm_name
    spl.control.create_group(group_name,vm_name,network_id)

def add_node(cmd):
    '''
    add one node to a group
    '''
    parts = spl.command_pattern.add.match(cmd)
    node_id = int(parts.group(1))
    group_name = parts.group(2)
    print 'add',node_id,'to',group_name
    spl.control.add_node_to_group(node_id,group_name)

def remove_node(cmd):
    '''
    remove one node from a group
    '''
    parts = spl.command_pattern.remove.match(cmd)
    node_id = int(parts.group(1))
    group_name = parts.group(2)
    print 'add',node_id,'to',group_name
    spl.control.remove_node_from_group(node_id,group_name)

def show_table(cmd):
    parts = spl.command_pattern.show_table.match(cmd)
    table = parts.group(1)
    if table not in class_name:
        print 'no such table'
        print 'available tables are:'
        for key in class_name:
            print key
        return
    spl.control.query_db(class_name[table])

def show_all():
    spl.control.query_db(spl.er.Node)
    spl.control.query_db(spl.er.Port)
    spl.control.query_db(spl.er.Network)
    spl.control.query_db(spl.er.VM)
    spl.control.query_db(spl.er.Switch)
    spl.control.query_db(spl.er.Group)
    spl.control.query_db(spl.er.User)

def auth(user_name,password):
    user = spl.control.get_entity_by_cond(spl.er.User,'user_name=="%s"'%(user_name))
    print user
    if not user:
        return False
    return user.password == password

def create_user(cmd):
    user_name,password = spl.command_pattern.create_user.match(cmd).groups()
    spl.control.create_user(user_name,password)
    

while True:
    user_name = raw_input('user:')
    password = raw_input("password:")
    if auth(user_name,password):
      spl.control.login_user(user_name)
      break
    print 'invalid user/password combination!'


while True:
    cmd = raw_input('spl>')
    if spl.command_pattern.create_group.match(cmd):
        create_group(cmd)
    elif cmd == 'show all':
        show_all()
    elif spl.command_pattern.destroy_group.match(cmd):
        print 'destroy a group'
    elif spl.command_pattern.show_group.match(cmd):
        print 'show group'
    elif spl.command_pattern.show_free_table.match(cmd):
        print 'free table'
    elif spl.command_pattern.show_table.match(cmd):
        show_table(cmd)
    elif spl.command_pattern.change_vlan.match(cmd):
        print 'ch vlan'
    elif spl.command_pattern.change_head.match(cmd):
        print 'ch head'
    elif spl.command_pattern.add.match(cmd):
        print 'add node'
        add_node(cmd)
    elif spl.command_pattern.remove.match(cmd):
        print 'remove node'
        remove_node(cmd)
    elif spl.command_pattern.create_user.match(cmd):
        create_user(cmd)
    elif cmd == 'exit':
        #Might need check before exit
        print 'Bye for now'
        exit()
    else:
        print 'invalid command'
        print 'usage'
        print spl.command_pattern.help_text
        
