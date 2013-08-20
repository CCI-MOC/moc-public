#!/usr/bin/python
#
# This script creates symlinks to the centos install pxe config for each
# machine listed in /etc/moc/machines.txt.

import os
import sys

for line in open("/etc/moc/machines.txt", "r"):
    macaddr, ipaddr = line.split(" ")
    linkname = "/var/lib/tftpboot/pxelinux.cfg/01-" + macaddr.replace(":", "-")
    os.system("ln -sfv ../centos/pxelinux.cfg " + linkname)
    os.system("power_cycle " + ipaddr)
