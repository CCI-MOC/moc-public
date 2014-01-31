"""This module provides routines for managing head nodes.

The exact API is currently in flux; We will attempt to make sure that
any given time the docstrings are accurate, but make no promises about
what it will say tomorrow.

Not everything is implemented to spec (or sometimes at all). Things
which are not are labeld as such (typically under the heading
"Conformance issues").
"""

import uuid
from subprocess import check_call as cmd
from spl import config

class Connection(object):
    """A connection to libvirtd"""

    def __init__(self, uri=None):
        """Create a connection to the libvirtd instance at `name`.

        `uri`, if provided, should be a libvirt uri, as documented at:

            http://libvirt.org/uri.html

        If a connection cannot be established, an `IOError` will be raised.

        Conformance issues:
        - An exception is never actually raised. currently we don't even
          establish a connection at this point, and so any failures
          will be silent.
        - `uri` is currently ignored.

        Questions:
        - do we even need a connection object? I start this when we were
          using the libvirt python api, but it's not clear we need this
          when we aren't establishing persistant connections. We may
          want to keep this here if we think we might transition to
          using the libvirt API, but frankly, I'm not sure there's a
          significant advantage in doing so.

          The only functionality this actually provides (or will) is the
          ability to specifiy non-default hypervisor uris. do we care?
        """
        pass

    def make_headnode(self):
        """Create and returns a new head node.

        The node will be a clone of the base image.

        Note that the node will not be started, merely created.
        the user must call the `start` method explicitly.

        returns a `HeadNode` object, corresponding to the created
        head node.
        """
        # uuid4 generates a uuid at random, as opposed to e.g. uuid1,
        # which generates one as a function of hostname & time.
        # Great variable names.
        name = 'headnode-%s' % uuid.uuid4()
        cmd(['virt-clone', '-o', 'base-headnode', '-n', name, '--auto-clone'])
        return HeadNode(name)

class HeadNode(object):
    """A head node virtual machine.

    Conformance issues:
    - The network interface stuff is currently unimplemented.
    """

    def __init__(self, name):
        """Clients of this module should *not* call this method directly.

        Instead, create a `Connection` and call `make_headnode()`.
        """
        self.name = name
        self.nics = []

    def start(self):
        """Start the vm"""
        cmd(['virsh', 'start', self.name])

    def stop(self):
        """Stop the vm.

        This does a hard poweroff; the OS is not given a chance to react.
        """
        cmd(['virsh', 'destroy', self.name])

    def add_nic(self, vlan_id):
        bridge = 'br-vlan%d' % vlan_id
        vlan_nic = '%s.%d' % (config.trunk_nic, vlan_id)
        vlan_id = str(vlan_id)
        cmd(['brctl', 'addbr', bridge])
        cmd(['vconfig', 'add', config.trunk_nic, vlan_id])
        cmd(['brctl', 'addif', bridge, vlan_nic])
        cmd(['virsh', 'attach-interface', self.name, 'bridge', bridge, '--config'])
        self.nics.append(vlan_id)

    def delete(self):
        """Delete the vm, including associated storage"""
        cmd(['virsh', 'undefine', self.name, '--remove-all-storage'])
        for nic in self.nics:
            nic = str(nic)
            bridge = 'br-vlan%d' % nic
            vlan_nic = '%s.%d' % (config.trunk_nic, nic)
            cmd(['brctl', 'delif', bridge, vlan_nic])
            cmd(['vconfig', 'rem', vlan_nic])
            cmd(['brctl', 'delbr', bridge])

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
        pass

    def set_interfaces(self, interfaces):
        """Set the vm's list of nics to `interfaces`.

        This will overwrite any previous network configuration. Any
        previously existing nics that are not in the list will be
        removed. If the vm is running, changes will not take effect
        until it is restarted.

        The argument to this function has the same semantics as the
        return value of `get_interfaces`.
        """
        pass


class Interface(object):
    """One of a virtual machine's network interface cards."""

    def __init__(self, vlan_id):
        """Create a new nic attached to vlan #vlan_id.

        The nic is an immutable object - once created it cannot be
        modified. Instead, a user wishing to reconfigure a vm should
        remove this interface and add a new one.
        """
        self.vlan_id = vlan_id

    def get_vlan(self):
        """Return the vlan number associated with this network card."""
        return self.vlan_id
