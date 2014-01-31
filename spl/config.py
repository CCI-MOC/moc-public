file_names={
    "node":"data/node.txt",
    "network":"data/network.txt",
    "vm":"data/vm.txt",
    "switch":"data/switch.txt",
    "port":"data/port.txt",
    "connect":"data/connect.txt",
    "user":"data/user.txt"
}

paths={
    # This should be the path to the virtio filesystems provided by death-star.
    # It will contain subdirectories named after the corresponding vlan id.
    "headnode-config" : "/var/lib/headnode-config",
}

trunk_nic = 'eth1'
