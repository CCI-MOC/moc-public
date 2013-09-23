#!/usr/bin/env python2

import socket, pdb

def remote_pdb(address=('0.0.0.0',9778)):
    '''
    Waits for a connection on `address`, which should be a streaming address
    suitable for passing to `socket.bind`, and attaches an instance of
    `pdb.Pdb` to it. The return value is the Pdb object.
    '''
    s = socket.socket()
    s.bind(address)
    s.listen(0)
    conn, _ = s.accept()
    cw = conn.makefile()
    return pdb.Pdb(stdin=cw, stdout=cw)
    


