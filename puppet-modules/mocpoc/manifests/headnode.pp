class mocpoc::headnode (
) {
	$tftpdir = '/var/lib/tftpboot'
	$syslinux_files = [
		"${tftpdir}/pxelinux.0",
		"${tftpdir}/menu.c32",
		"${tftpdir}/memdisk",
		"${tftpdir}/mboot.c32",
		"${tftpdir}/chain.c32",
	]
	# We need a few packages for our head nodes:
	package { [
		'isc-dhcp-server',
		'tftpd-hpa',
		'syslinux-common',
		'fcgiwrap',
		'nginx',
		] :
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
	# Mount the virtio filesystem on boot (This doesn't seem to work from fstab):
	file { '/etc/rc.local':
		content => '
		mount -t 9p -o ro,trans=virtio /etc/moc /etc/moc
		'
	}
	# TODO:
	# - most of /var/lib/tftpboot/centos.
	#
	#   Conceptually, we want something like this, to grab the boot images for
	#   centos:
	#
	#   $centos_mirror = 'http://mirror.mit.edu/centos/6.4/os/x86_64/'
	#   file { "${tftpdir}/centos/vmlinuz":
	#   	source => "${centos_mirror}/isolinux/vmlinuz",
	#   }
	#   file { "${tftpdir}/centos/initrd.img":
	#   	source => "${centos_mirror}/isolinux/initrd.img",
	#   }
	#
	#   Unfortunately, this won't work since puppet can't use an http url as a
	#   source. It's also at least questionable from a security standpoint.
	# - iptables
	# - puppet master
	# - python-mocutils
}
