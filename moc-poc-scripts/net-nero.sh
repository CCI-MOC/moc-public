#!/bin/sh -e
#
# This sets up (or shuts down) the network for a two node openstack setup.
#
# the network topology will look as follows:
#
# [host] <eth1> --- <br1>              [slave]
#                     |                 <tap2>
#                     |                   |
#                     |                 <br2>
#                     |                   |
#                     |                 <tap3>
#                     +------ <tap1> - [master]
#
# legend:
#   <brX>  # bridge
#   <tapX> # vm interface
#   <eth1>  # host machine's external ethernet.
#   [host] # A host
#
# We need uml-utilities (for tunctl) and bridge-utils (for brctl), in order
# for this to work.
#
# run with an argument of 'start' to set up the network, or 'stop' to tear it down.

case "$1" in
	start)
		## set up the network

		# set up eth1 as promiscuous.
		sudo ip link set eth1 up
		sudo ip link set promisc on dev eth1

		# create vm interfaces, owned by the current user.
		sudo tunctl -u $USER -t tap1
		sudo tunctl -u $USER -t tap2
		sudo tunctl -u $USER -t tap3

		# create the bridges
		sudo brctl addbr br1
		sudo brctl addbr br2

		# assign a fixed mac address to br1 - otherwise we'll get a
		# different ip from dhcp each time we start the network.
		sudo ip link set address 06:55:54:fe:ca:59 dev br1

		# set up the external bridge (br1).
		sudo brctl addif br1 tap1
		sudo brctl addif br1 eth1

		# set up the internal brige (br2).
		sudo brctl addif br2 tap2
		sudo brctl addif br2 tap3

		# bring up variuos interfaces
		for iface in br1 br2 tap1 tap2 tap3 ; do
			sudo ip link set $iface up
		done

		# bring up host networking. We'll use the bridge the host
		# interface is connected to.
		sudo dhclient br1

	;;
	stop)
		## tear down the network

		# bring down the interfaces
		for iface in eth1 br1 br2 tap1 tap2 tap3; do
			sudo ip link set $iface down
		done
		# remove everything from the bridges
		sudo brctl delif br1 tap1
		sudo brctl delif br1 eth1

		sudo brctl delif br2 tap2
		sudo brctl delif br2 tap3

		# delete the vm interfaces
		sudo tunctl -d tap1
		sudo tunctl -d tap2
		sudo tunctl -d tap3

		# delete the bridges
		sudo brctl delbr br1
		sudo brctl delbr br2

	;;
	restart)
		$0 stop && sleep 1 && $0 start
	;;
	*)
		echo "usage : $0 {start|stop|restart}" >&2
	;;
esac
