#!/usr/bin/pyton

import sys, os, sqlite3, re, itertools
import switch_controls


class DB_Controller:
  
  def __init__(self, db):
    # Check if the db already exists
    new = not os.path.exists(db)
    
    # Build the connection to the db
    self.conn = sqlite3.connect(db)
    
    if new:
      self._create_tables()
      # Add init machines
      for line in open(raw_input("File of machine listing:"), 'r'):
        line = line.rstrip()
        node_id, mac, node_ip = line.split(' ')
        self.add_machine_to_db(node_id, mac, node_ip)
      # Add init vlans
      for vlan in raw_input("Vlan list:").split(','):
        if '-' not in vlan:
          self.add_remove_vlan_to_db(int(vlan), True)
        else:
          parts = vlan.split('-')
          map(lambda x: self.add_remove_vlan_to_db(x, True), range(int(parts[0]), int(parts[1])+1))
      # Add init head nodes
      for name in open(raw_input("File of head node listing:"), 'r'):
        self.add_head_node_to_db(name.rstrip())
    
    # Now we want to query the switch and ensure that the db and switch agree
    # If the db has more than switch, alert user to problem
    # Print switch and db states, and ask who should adopt what
    # If switch has more than db, alert unowned vlans, but allow to continue
    
    return
  
  
  def _create_tables(self):
    # For initializing a non-existant db
    c = self.conn.cursor()
    c.execute('''CREATE TABLE nodes
	  (node_id integer primary key, mac_addr string, manage_ip string, available integer, group_name string)''')
    c.execute('''CREATE TABLE groups
	  (group_name string primary key, vlan_id integer, vm_name string)''')
    c.execute('''CREATE TABLE vlans
	  (vlan_id integer primary key, available integer)''')
    c.execute('''CREATE TABLE vms
	  (vm_name string primary key, available integer)''')
  
  
  def show_group(self, name):
    if not self.check_exists('groups', 'group_name', name):
      print "Group", name, "does not exist"
      return
    c = self.conn.cursor()
    c.execute('select * from groups where group_name = ?', (name,))
    print 'Group:\n', c.fetchone()
    print 'Nodes:'
    c.execute('select * from nodes where group_name = ?', (name,))
    for row in c.fetchall():
      print row
    print ''
    
  
  def show_db(self, free, spec_table=''):
    # Open two cursors into the db
    # Unfortunately 2 are needed to manage 2 loops
    c = self.conn.cursor()
    tmp = self.conn.cursor()
    # Select and loop over all the tables
    tmp.execute("select name from sqlite_master where type = 'table'")
    print ''
    for table in tmp.fetchall():
      table = table[0]
      
      if free and table == 'groups':
        continue
      if spec_table and table != spec_table:
        continue
      print table
      # Select and print all the column names from the current table
      c.execute("PRAGMA table_info(" + table +")")
      for column in c.fetchall():
	print column[1], '|', 
      print ''
      # Select every row from the current table and print it (if free)
      c.execute("select * from " + table)
      ### Warning: Cluster fuck below, to be fixed later, functional for now
      # Problem is getting val_name, fix db entries?
      for row in c.fetchall():
	if free:
	  if table == "nodes":
	    if self.check_available(table, "node_id", row[0]):
	      print row
	  elif table == "vlans":
	    if self.check_available(table, "vlan_id", row[0]):
	      print row
	  elif table == "vms":
	    if self.check_available(table, "vm_name", row[0]):
	      print row
	else:
	  print row
      print ''


  def check_exists(self, table, val_name, val_id):
    c = self.conn.cursor()
    c.execute("SELECT EXISTS(SELECT 1 FROM " + table + "  WHERE " + val_name + "=? LIMIT 1)", (val_id,))
    return c.fetchone()[0]
  
  def check_available(self, table, val_name, val_id):
    # First make sure it exists
    if not self.check_exists(table, val_name, val_id):
      print val_name, val_id, "does not exist"
      return
    c = self.conn.cursor()
    # Checks if the desired value is available for allocation
    c.execute('select available from ' + table + ' where ' + val_name + ' = ?', (val_id,))
    return c.fetchone()[0]


  def add_machine_to_db(self, node_id, mac, node_ip):
    # Make sure the node_id isn't already taken
    if self.check_exists('nodes', 'node_id', node_id):
      print "node_id", node_id, "is already taken"
      return
    c = self.conn.cursor()
    c.execute('''INSERT INTO nodes
        values(?,?,?,1,'none')''', (node_id, mac, node_ip,))
  
  def add_remove_vlan_to_db(self, vlan_id, add):
    # Make sure this isn't already a vlan
    exists = self.check_exists('vlans', 'vlan_id', vlan_id)
    if add and exists or not (add or exists):
      print "Error: vlan_id", vlan_id, "not available"
      return
    c = self.conn.cursor()
    if add:
      c.execute('''INSERT INTO vlans values(?,1)''',(vlan_id,))
    else:
      c.execute('delete from vlans where vlan_id = ?', (vlan_id,))
    return

  def add_head_node_to_db(self, name):
    # Make sure the head_node isn't already taken
    if self.check_exists('vms', 'vm_name', name):
      print "head_node_id", name, "is already taken"
      return
    c = self.conn.cursor()
    c.execute('''INSERT INTO vms values(?,1)''', (name,))

  
  def create_group(self, group_name, vlan_id, vm_name):
    try:
      # Make sure that there isn't already a group with this name
      if self.check_exists('groups', 'group_name', group_name):
	print "Group", group_name, "already exists."
	return False

      # Make sure that the vlan asked for is available
      if not self.check_available('vlans', 'vlan_id', vlan_id):
	print "vlan id not available"
	return False
      # Make sure that the vm asked for is available
      if not self.check_available('vms', 'vm_name', vm_name):
	print "vm not available"
	return False

      c = self.conn.cursor()
      c.execute('update vlans set available = 0 where vlan_id = ?', (vlan_id,))
      c.execute('update vms set available = 0 where vm_name = ?', (vm_name,))
      c.execute('insert into groups values(?,?,?)', (group_name, vlan_id, vm_name,))

      return True
    except:
      print "Creating group failed."
      print "Unexpected error:", sys.exc_info()[0]
      return False

  def remove_group(self, group_name):
    try:
      # Ensure that group_name is a valid group
      if not self.check_exists('groups', 'group_name', group_name):
	print "Group", group_name, "does not exist."
	return False

      # Get the vlan_id and vm_name from this group
      c = self.conn.cursor()
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
      print "Unexpected error:", sys.exc_info()[0]
      return False


  def move_nodes_group(self, node_ids, group_name, add):
    # Unroll the group name and node we want
    for node_id in node_ids.split(','):
      node_id = int(node_id)

      # Make sure that the node asked for is available
      if add and not self.check_available('nodes', 'node_id', node_id):
	print "ERROR: node id", node_id, "not available"
	continue

      # Add / remove the node from the desired group
      c = self.conn.cursor()
      c.execute('update nodes set available=?, group_name=? where node_id=?', (1-add, group_name, node_id,))
    return True


  def change_vlan(self, group_name, vlan_id):
    # Make sure the group exists
    if not self.check_exists('groups', 'group_name', group_name):
      print "Group", group_name, "does not exist."
      return
    # Make sure the new vlan wanted is available
    if not self.check_available('vlans', 'vlan_id', vlan_id):
      print "Vlan", vlan_id, "not available"
      return
    c = self.conn.cursor()
    # Get the old vlan to be marked as available
    c.execute('select vlan_id from groups where group_name = ?', (group_name,))
    old = c.fetchone()[0]
    # Update the group
    c.execute('update groups set vlan_id=? where group_name=?', (vlan_id, group_name,))
    # Toggle availability
    c.execute('update vlans set available=0 where vlan_id=?', (vlan_id,))
    c.execute('update vlans set available=1 where vlan_id=?', (old,))

  def change_head(self, group_name, vm_name):
    # Make sure the group exists
    if not self.check_exists('groups', 'group_name', group_name):
      print "Group", group_name, "does not exist."
      return
    # Make sure the new vlan wanted is available
    if not self.check_available('vms', 'vm_name', vm_name):
      print "Vm", vm_name, "not available"
      return
    c = self.conn.cursor()
    # Get the old vlan to be marked as available
    c.execute('select vm_name from groups where group_name = ?', (group_name,))
    old = c.fetchone()[0]
    # Update the group
    c.execute('update groups set vm_name=? where group_name=?', (vm_name, group_name,))
    # Toggle availability
    c.execute('update vms set available=0 where vm_name=?', (vm_name,))
    c.execute('update vms set available=1 where vm_name=?', (old,))

 
  def deploy(self):
    # Remove machines to be moved from old vlans
    # Remove vlans to be deleted
    # Create new vlans
    c = self.conn.cursor()
    c.execute('select * from groups')
    vlans = ""
    for group in c.fetchall():
      # Make the vlan for this group
      vlan_id = str(group[1])
      switch_controls.make_remove_vlans(vlan_id, True)

      # Get the nodes assigned to this group
      c.execute('select node_id from nodes where group_name=?',(group[0],))
      nodes = ""
      for node in c.fetchall():
	nodes += str(node[0]) + ","
      # Ensure that death-star is on all
      nodes += '16'
      # Add the ports to the vlan
      switch_controls.edit_ports_on_vlan(nodes, vlan_id, True)
      
      # Write to the vm-shared memory
      vm_name = group[2]
      try:
        os.mkdir('/var/lib/headnode-config/' + vlan_id)
      except:
        pass
      f = open('/var/lib/headnode-config/' + vlan_id + '/machines.txt', 'w+')
      #f = open('./vms/' + vm_name + '.txt', 'w+')
      c.execute('select mac_addr, manage_ip from nodes where group_name=?',(group[0],))
      for row in c.fetchall():
        f.write(row[0] + ' ' + row[1] + '\n')
      f.close()
      os.system("vm-vlan up " + vlan_id + " " + vm_name)
    self.conn.commit()


