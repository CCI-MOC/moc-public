class mocpoc::headnode (
) {

	$syslinux_files = [
		'/var/lib/tftpboot/pxelinux.0',
		'/var/lib/tftpboot/menu.c32',
		'/var/lib/tftpboot/memdisk',
		'/var/lib/tftpboot/mboot.c32',
		'/var/lib/tftpboot/chain.c32',
	]
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
		require => Package['isc-dhcp-server'],
	}
	# We need this directory to exist for a number of things:
	file { '/var/lib/tftpboot/pxelinux.cfg':
		ensure => 'directory',
		require => Package['tftpd-hpa'],
	}
	Package['tftpd-hpa'] -> File[$syslinux_files]
	Package['syslinux-common'] -> File[$syslinux_files]

	# Copy the bootloader into the tftp directory:
	file { '/var/lib/tftpboot/pxelinux.0':
		source => '/usr/lib/syslinux/pxelinux.0',
	}
	file { '/var/lib/tftpboot/menu.c32':
		source => '/usr/lib/syslinux/menu.c32',
		require => Package['syslinux-common'],
	}
	file { '/var/lib/tftpboot/memdisk':
		source => '/usr/lib/syslinux/memdisk',
	}
	file { '/var/lib/tftpboot/mboot.c32':
		source => '/usr/lib/syslinux/mboot.c32',
	}
	file { '/var/lib/tftpboot/chain.c32':
		source => '/usr/lib/syslinux/chain.c32',
	}
	# make sure dhcpd is configured correctly:
	file { '/etc/dhcp/dhcpd.conf':
		source => 'puppet:///modules/mocpoc/headnode/dhcpd.conf',
		require => Package['isc-dhcp-server'],
	}
	# make sure the network setup is correct:
	file { '/etc/network/interfaces':
		source => 'puppet:///modules/mocpoc/headnode/interfaces',
	}
	# boot nodes to the disk by default:
	file { '/var/lib/tftpboot/pxelinux.cfg/default':
		content => '
		default disk
		label disk
			LOCALBOOT 0
		',
		require => File['/var/lib/tftpboot/pxelinux.cfg'],
	}
	# make the tftp directory available via http as well - this is needed for kickstart to work:
	file { '/etc/nginx/sites-enabled/tftp':
		source => 'puppet:///modules/mocpoc/headnode/nginx-tftp',
		require => Package['nginx'],
	}
	# TODO:
	# - mount /etc/moc
	# - most of /var/lib/tftpboot/centos
	# - iptables
	# - puppet master
	# - python-mocutils
}
