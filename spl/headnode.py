"""This module provides routines for managing head nodes."""

import libvirt


class Connection(object):
    """a connection to libvirtd"""

    def __init__(self, name=None):
        """creates a connection to the libvirtd instance at `name`.

        `name` should be a libvirt uri, as documented at:

            http://libvirt.org/uri.html

        If a connection cannot be established, an `IOError` will be raised.
        """
        self.conn = libvirt.virConnectOpen(name)
        if self.conn is None:
            raise IOError('Could not connect to libvirt (uri=%s).' % name)


class HeadNode(object):
    """A head node virtual machine."""

    def __init__(self, conn):
        """creates a new head node

        `conn` is a `Connection`. The head node created will be managed
        by the associated libvirtd instance.

        Note that the head node will not be started, merely created.
        the user must call the `start` method explicitly.
        """
        pass

    def start(self):
        """starts the vm"""
        pass
