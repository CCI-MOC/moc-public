"""This module provides routines for managing head nodes."""

import libvirt


class Connection(object):
    """A connection to libvirtd"""

    def __init__(self, name=None):
        """Create a connection to the libvirtd instance at `name`.

        `name` should be a libvirt uri, as documented at:

            http://libvirt.org/uri.html

        If a connection cannot be established, an `IOError` will be raised.
        """
        self.conn = libvirt.virConnectOpen(name)
        if self.conn is None:
            raise IOError('Could not connect to libvirt (uri=%s).' % name)

    def make_headnode(self):
        """Create and returns a new head node.

        The node will be a clone of the base image.

        Note that the node will not be started, merely created.
        the user must call the `start` method explicitly.
        """


class HeadNode(object):
    """A head node virtual machine."""

    def start(self):
        """Start the vm"""
        pass

    def stop(self):
        """Stop the vm.

        This does a hard poweroff; the OS is not given a chance to react.
        """
        pass

    def delete(self):
        """Delete the vm, including associated storage"""
        pass

    def get_interfaces(self):
        """Return a list of the vm's network interfaces.

        The members of the list will be instances of `Interface`. the
        index of each interface reflects the order of the interfaces as
        seen by the vm, i.e. (typically, though it depends on the guest),
        in interfaces list ints, ints[0] will be eth0, ints[1] will be
        eth1, and so on.

        Modification of this list *will not* affect the vm in any way;
        to update the configuration, use `set_interfaces`.
        """

    def set_interfaces(self, interfaces):
        """Set the vm's list of nics to `interfaces`.

        This will overwrite any previous network configuration. Any
        previously existing nics that are not in the list will be
        removed. If the vm is running, changes will not take effect
        until it is restarted.

        The argument to this function has the same semantics as the
        return value of `get_interfaces`.
        """


class Interface(object):
    """One of a virtual machine's network interface cards."""

    def __init__(self, vlan_id):
        """Create a new nic attached to vlan #vlan_id.

        The nic is an immutable object - once created it cannot be
        modified. Instead, a user wishing to reconfigure a vm should
        remove this interface and add a new one.
        """
        pass

    def get_vlan(self):
        """Return the vlan number associated with this network card."""
        pass
