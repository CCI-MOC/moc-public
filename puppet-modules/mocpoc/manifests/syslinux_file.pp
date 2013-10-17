# A defined type for the syslinux boot files which are copied from the
# syslinux-common package.
define mocpoc::syslinux_file ($filename = $title) {
	file { "/var/lib/tftpboot/$filename":
		source => "/usr/lib/syslinux/$filename",
		require => Package['syslinux-common', 'tftpd-hpa'],
	}
}
