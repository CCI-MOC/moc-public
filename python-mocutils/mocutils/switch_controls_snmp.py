#! /usr/bin/python
import os

def make_remove_vlans(vlan_ids,add,switch_ip='192.168.0.1',community='admin'):
	# Expects that you send a string which is a comma separated list of vlan_ids and a bool for adding or removing
	OID_portVlanId='1.3.6.1.4.1.11863.1.1.4.3.1.1.2.1.1'
	OID_portVlanStatus='1.3.6.1.4.1.11863.1.1.4.3.1.1.2.1.6'
	for vlan_id in vlan_ids.split(','):
		if add:
			os.system('snmpset -v1 -c'+community+' '+switch_ip+' '+OID_portVlanId+'.'+vlan_id+' i '+vlan_id)
			os.system('snmpset -v1 -c'+community+' '+switch_ip+' '+OID_portVlanStatus+'.'+vlan_id+' i 4')
		else:
			os.system('snmpset -v1 -c'+community+' '+switch_ip+' '+OID_portVlanStatus+'.'+vlan_id+' i 6')
def edit_ports_on_vlan(port_ids,vlan_id,add,switch_ip='192.168.0.1',community='admin'):
	# Expects that you send a comma separated list of ports
 	# A string for vlan_id
  	# And a bool for adding (True = adding, False = Removing)
	OID_vlanUntagPortMemberAdd='1.3.6.1.4.1.11863.1.1.4.3.1.1.2.1.4'
	OID_vlanPortMemberRemove='1.3.6.1.4.1.11863.1.1.4.3.1.1.2.1.5'
	if add:
		os.system('snmpset -v1 -c'+community+' '+switch_ip+' '+OID_vlanUntagPortMemberAdd+'.'+vlan_id+' s '+'"'+port_ids+'"')
	else:
		os.system('snmpset -v1 -c'+community+' '+switch_ip+' '+OID_vlanPortMemberRemove+'.'+vlan_id+' s '+'"'+port_ids+'"')
