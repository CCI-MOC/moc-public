#! /usr/bin/python
import os
def get_dot10said(vlan_id):
        #expect vlan_id as a str
        dot10said=100000+int(vlan_id)
	#print dot10said
	dot10said="%x"%(dot10said)
	return dot10said.zfill(8)
def make_remove_vlans(vlan_ids,add,switch_ip='192.168.0.254'):
	# Expects that you send a string which is a comma separated list of vlan_ids and a bool for adding or removing
	for vlan_id in vlan_ids.split(','):
		if add:
			dot10said=get_dot10said(vlan_id)
			print dot10said
			os.system('snmpset -v2c -c private '+switch_ip+' vtpVlanEditOperation.1 i 2')
			os.system('snmpset -v2c -c private '+switch_ip+' vtpVlanEditRowStatus.1.'+vlan_id+' i 4')
			os.system('snmpset -v2c -c private '+switch_ip+' vtpVlanEditType.1.'+vlan_id+' i 1')
			os.system('snmpset -v2c -c private '+switch_ip+' vtpVlanEditName.1.'+vlan_id+' s "vlan_'+vlan_id+'"')

			#Below is to set a strange(?) so-called dot10said, which is a hex of 100000+vlan_id
			os.system('snmpset -v2c -c private '+switch_ip+' vtpVlanEditDot10Said.1.'+vlan_id+' x '+dot10said)
			os.system('snmpset -v2c -c private '+switch_ip+' vtpVlanEditOperation.1 i 3')
		else:
			os.system('snmpset -v2c -c private '+switch_ip+' vtpVlanEditOperation.1 i 2')
			os.system('snmpset -v2c -c private '+switch_ip+' vtpVlanEditRowStatus.1.'+vlan_id+' i 6')
			os.system('snmpset -v2c -c private '+switch_ip+' vtpVlanEditOperation.1 i 3')
def edit_ports_on_vlan(port_ids,vlan_id,add,switch_ip='192.168.0.254'):
	
	# Expects that you send a comma separated list of ports
 	# A string for vlan_id
  	# And a bool for adding (True = adding, False = Removing)
	for port_id in port_ids.split(','):
		ifIndex=int(port_id)+1
		ifIndex=str(ifIndex)
		#The ifIndex for FastEthernet0/1 is 2, for FastEthernet0/48 is 49. Except the 48 FastEthernet ports. 
		#There are two ports GigabitEthernet0/1 and GigabitEthernet0/2
		if add:
			os.system('snmpset -v2c -c private '+switch_ip+' vmVlan.'+ifIndex+' i '+vlan_id)
		else:
		#remove the port by setting it to belong to the default vlan 1
			os.system('snmpset -v2c -c private '+switch_ip+' vmVlan.'+ifIndex+' i 1')

