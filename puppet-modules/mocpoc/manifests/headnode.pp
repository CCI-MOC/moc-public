# Sets up an ubuntu 12.04 machine as a headnode for mocpoc-head.
#
# Parameters:
# [slave_rootpw]: the encrypted root password to use on slave nodes (mandatory).
class mocpoc::headnode (
	$slave_rootpw,
) {
	$tftpdir = '/var/lib/tftpboot'
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
	# Create subdirectories in the tftp root.
	file { [
		"${tftpdir}/pxelinux.cfg",
		"${tftpdir}/centos"
		] :
		ensure => 'directory',
		require => Package['tftpd-hpa'],
	}
	file { "${tftpdir}/centos/ks.cfg":
		require => File["${tftpdir}/centos"],
		content => template('mocpoc/ks.cfg.erb'),
	}
	file { "${tftpdir}/centos/vmlinuz":
		require => File["${tftpdir}/centos"],
		source => 'puppet:///modules/mocpoc/headnode/vmlinuz',
	}
	file { "${tftpdir}/centos/initrd.img":
		require => File["${tftpdir}/centos"],
		source => 'puppet:///modules/mocpoc/headnode/initrd.img',
	}
	file { "${tftpdir}/centos/pxelinux.cfg":
		require => File["${tftpdir}/centos"],
		source => 'puppet:///modules/mocpoc/headnode/pxelinux.cfg-centos',
	}

	# Copy the bootloader into the tftp directory:
	mocpoc::syslinux_file { [
		'pxelinux.0',
		'menu.c32',
		'memdisk',
		'mboot.c32',
		'chain.c32',
	] : }
	# make sure dhcpd is configured correctly:
	file { '/etc/dhcp/dhcpd.conf':
		source => 'puppet:///modules/mocpoc/headnode/dhcpd.conf',
		require => Package['isc-dhcp-server'],
	}
	# make sure the network setup is correct:
	file { '/etc/network/interfaces':
		source => 'puppet:///modules/mocpoc/headnode/interfaces',
		notify => Service['networking'],
	}
	file { '/etc/iptables':
		source => 'puppet:///modules/mocpoc/headnode/iptables',
		notify => Service['networking'],
	}
	# boot nodes to the disk by default:
	file { "${tftpdir}/pxelinux.cfg/default":
		content => '
		default disk
		label disk
			LOCALBOOT 0
		',
		require => File["${tftpdir}/pxelinux.cfg"],
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

	service { [
		'networking',
		'nginx',
		'isc-dhcp-server',
		'tftpd-hpa',
		] :
		ensure => running,
	}
	# TODO:
	# - puppet master
	# - python-mocutils
}
