#!/usr/bin/env python

import cgi, cgitb, re, os

# This will log any errors.
cgitb.enable()

form = cgi.FieldStorage()
mac = form.getfirst("mac", "").lower().replace(':', '-')

# This should match mac address with 
if re.match('^([0-9a-f]{2}-){5}[0-9a-f]{2}$', mac) != None:
    try:
        os.remove('/var/lib/tftpboot/pxelinux.cfg/01-' + mac)
        print 'Content-Type: text/plain\n'
        print 'OK'
    except OSError:
        print 'Content-Type: text/plain'
        print 'Status: 400\n'
        print 'Error: file not found'
else:
    print 'Content-Type: text/plain'
    print 'Status: 400\n'
    print 'Error: invalid mac address'
