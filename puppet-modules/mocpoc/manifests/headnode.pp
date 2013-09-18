class headnode (
) {
	# We need a few packages for our head nodes:
	package { 'isc-dhcp-server':
		ensure => 'installed',
	}
	package { 'tftpd-hpa':
		ensure => 'installed',
	}
	package { 'syslinux-common':
		ensure => 'installed',
	}
	package { 'fcgiwrap':
		ensure => 'installed',
	}
	package { 'nginx':
		ensure => 'installed',
	}
	# We only want the dhcp server listening on eth0. This file handles that:
	file { '/etc/default/isc-dhcp-server':
		content => 'INTERFACES="eth0"\n',
	}
	# Copy the bootloader into the tftp directory:
	file { '/var/lib/tftpboot/pxelinux.cfg/pxlinux.0':
		source => '/usr/lib/syslinux/pxelinux.0',
	}
	file { '/var/lib/tftpboot/pxelinux.cfg/menu.c32':
		source => '/usr/lib/syslinux/menu.c32',
	}
	file { '/var/lib/tftpboot/pxelinux.cfg/memdisk':
		source => '/usr/lib/syslinux/memdisk',
	}
	file { '/var/lib/tftpboot/pxelinux.cfg/mboot.c32':
		source => '/usr/lib/syslinux/mboot.c32',
	}
	file { '/var/lib/tftpboot/pxelinux.cfg/chain.c32':
		source => '/usr/lib/syslinux/chain.c32',
	}
	# make sure dhcpd is configured correctly:
	file { '/etc/dhcp/dhcpd.conf':
		source => 'puppet:///modules/mocpoc/headnode/dhcpd.conf',
	}
	# make sure the network setup is correct:
	file { '/etc/network/interfaces':
		source = 'puppet:///modules/mocpoc/headnode/interfaces',
	}
	# boot nodes to the disk by default:
	file { '/var/lib/tftpboot/pxelinux.cfg/default':
		content => '
		default disk
		label disk
			LOCALBOOT 0
		',
	}
	# make the tftp directory available via http as well - this is needed for kickstart to work:
	file { '/etc/nginx/sites-enabled/tftp':
		source => 'puppet:///modules/mocpoc/headnode/nginx-tftp',
	}
	# TODO:
	# - mount /etc/moc
	# - most of /var/lib/tftpboot/centos
	# - iptables
	# - puppet master
	# - python-mocutils
}
