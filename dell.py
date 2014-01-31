#! /usr/bin/python
import os


def make_remove_vlans(vlan_ids,add,switch_ip='192.168.3.245'):
    # Expects that you send a string which is a comma separated list of vlan_ids and a bool for adding or removing
    for vlan_id in vlan_ids.split(','):
        if add:
            cmd='''snmpset -v1 -cDell_Network_Manager 192.168.3.245 \
dot1qVlanStaticName.%s s "%s" \
dot1qVlanStaticEgressPorts.%s x '00' \
dot1qVlanForbiddenEgressPorts.%s x '00' \
dot1qVlanStaticUntaggedPorts.%s x '00' \
dot1qVlanStaticRowStatus.%s i 4'''%(vlan_id,"vlan"+vlan_id,vlan_id,vlan_id,vlan_id,vlan_id)
            print cmd
            os.system(cmd)
#os.system(cmd)
        else:
           pass
def edit_ports_on_vlan(port_ids,vlan_id,add,switch_ip='192.168.3.245'):
    
    # Expects that you send a comma separated list of ports
    # A string for vlan_id
    # And a bool for adding (True = adding, False = Removing)
    x=0
    for port_id in port_ids.split(','):
        if add:
            port=int(port_id)
            x=x+2**(24-port)
        else:
            pass

    hexstr="%x"%x
    hexstr=hexstr.zfill(6)
    cmd='''snmpset -v1 -cDell_Network_Manager 192.168.3.245 \
dot1qVlanStaticEgressPorts.%s x '%s' \
dot1qVlanStaticUntaggedPorts.%s x '%s' '''%(vlan_id,hexstr,vlan_id,hexstr)
    print cmd
    os.system(cmd)
