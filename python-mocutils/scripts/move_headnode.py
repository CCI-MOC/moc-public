#!/usr/bin/env python

"""
Move a head node to a new vlan.

This module can be invoked from the shell, in which case the parameters to the
move_headnode function are taken from the first two command line arguments.

"""

import xml.etree.ElementTree as ET
import sys, os

def move_headnode(vlan_id, filename):
    """
    Edits the configuration vm configuration file `filename` such that the vm
    is moved to the vlan with id `vlan_id`
    """
    # We need to change two things in the config - the path to the filesystem
    # to be mounted as /etc/moc, and vlan that the vm is attached to.
    tree = ET.parse(filename)
    root = tree.getroot()
    devices = root.find('devices')
    filesystem = devices.find('filesystem')
    nics = devices.findall('interface')
    for nic in nics:
        nic_source = nic.find('source')
        # We only want to change the nic attached to the private network; br0
        # is the public.
        if nic_source.attrib['bridge'] != 'br0':
            nic_source.attrib['bridge'] = 'br' + vlan_id
    fsys_source = filesystem.find('source')
    fsys_source.attrib['dir'] = os.path.dirname(fsys_source.attrib['dir']) + '/' + vlan_id
    tree.write(filename)

if __name__ == '__main__':
    move_headnode(sys.argv[1], sys.argv[2])
