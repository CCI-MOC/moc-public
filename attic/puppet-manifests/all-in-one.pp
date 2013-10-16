#
# This document serves as an example of how to deploy
# basic single-node openstack environments.
#
# These manifest is a altered version of:
# puppet/modules/openstack/examples/site.pp
#

# deploy a script that can be used to test nova
class { 'openstack::test_file': }

####### variables ##################

######### change interfaces accordingly!
# assumes that eth0 is the public interface
$public_interface        = 'eth1'
$public_address          = $ipaddress_eth1
# assumes that eth1 is the interface that will be used for the vm network
# this configuration assumes this interface is active but does not have an
# ip address allocated to it.
$private_interface       = 'eth0'
# credentials
$admin_email             = 'root@localhost'
$admin_password          = 'replace_paswd'
$keystone_db_password    = 'replace_paswd'
$keystone_admin_token    = 'replace_paswd'
$nova_db_password        = 'replace_paswd'
$nova_user_password      = 'replace_paswd'
$glance_db_password      = 'replace_paswd'
$glance_user_password    = 'replace_paswd'
$rabbit_password         = 'replace_paswd'
$rabbit_user             = 'rabbituser'
$fixed_network_range     = '10.0.0.0/24'
# $floating_network_range  = '192.168.101.64/28'
# switch this to true to have all service log at verbose
$verbose                 = false
# by default it does not enable atomatically adding floating IPs
$auto_assign_floating_ip = false

$libvirt_type            = 'kvm'
$mysql_root_password     = 'replace_paswd'
$secret_key              = 'replace_paswd'
$havequantum		 = false
$havecinder		 = true
$cinder_user_password    = 'replace_paswd'
$cinder_db_password      = 'replace_paswd'

#### end variables #################

# all nodes whose certname matches openstack_all should be
# deployed as all-in-one openstack installations.
node /openstack_all/ {

  include 'apache'

  class { 'openstack::all':
    public_address          => $public_address,
    public_interface        => $public_interface,
    private_interface       => $private_interface,
    admin_email             => $admin_email,
    admin_password          => $admin_password,
    keystone_db_password    => $keystone_db_password,
    keystone_admin_token    => $keystone_admin_token,
    nova_db_password        => $nova_db_password,
    nova_user_password      => $nova_user_password,
    glance_db_password      => $glance_db_password,
    glance_user_password    => $glance_user_password,
    rabbit_password         => $rabbit_password,
    libvirt_type            => $libvirt_type,
    floating_range          => $floating_network_range,
    fixed_range             => $fixed_network_range,
    verbose                 => $verbose,
    auto_assign_floating_ip => $auto_assign_floating_ip,
    mysql_root_password     => $mysql_root_password, 
    secret_key              => $secret_key,
    quantum                 => $havequantum,
    cinder                  => $havecinder,
    cinder_user_password    => $cinder_user_password,
    cinder_db_password      => $cinder_db_password,
  }

  class { 'openstack::auth_file':
    admin_password       => $admin_password,
    keystone_admin_token => $keystone_admin_token,
    controller_node      => '127.0.0.1',
  }

}
