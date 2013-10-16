#
# This document serves as an example of how to deploy
# basic single and multi-node openstack environments.
#

# This version is specific to a test setup with three nodes: 9 (controller),
# and 11 and 13 (compute).  For other setups, you must change the lines
# labelled CHANGEME


# deploy a script that can be used to test nova
class { 'openstack::test_file': }

####### shared variables ##################


# this section is used to specify global variables that will
# be used in the deployment of multi and single node openstack
# environments

# assumes that eth0 is the public interface
$public_interface        = 'eth1'
# assumes that eth1 is the interface that will be used for the vm network
# this configuration assumes this interface is active but does not have an
# ip address allocated to it.
$private_interface       = 'eth0'
# credentials
$admin_email             = 'root@localhost'
$admin_password          = 'changeme'
$keystone_db_password    = 'changeme'
$keystone_admin_token    = 'changeme'
$nova_db_password        = 'changeme'
$nova_user_password      = 'changeme'
#$quantum_db_password        = 'changeme'
#$quantum_user_password      = 'changeme'
$glance_db_password      = 'changeme'
$glance_user_password    = 'changeme'
$rabbit_password         = 'changeme'
$rabbit_user             = 'openstack_rabbit_user'
# $fixed_network_range     = '10.0.0.0/24'
$fixed_network_range     = '192.168.15.0/24'
# switch this to true to have all service log at verbose
$verbose                 = false
# by default it does not enable atomatically adding floating IPs
$auto_assign_floating_ip = false


## JUST ADDED
$libvirt_type            = 'kvm'
$mysql_root_password     = 'changeme'
$secret_key              = 'changeme'
$havequantum  	 = false
$havecinder		 = false
$cinder_user_password    = 'changeme'
$cinder_db_password      = 'changeme'
## JUST ADDED


#### end shared variables #################

# all nodes whose certname matches openstack_all should be
# deployed as all-in-one openstack installations.

### REMOVED ###

# multi-node specific parameters

$controller_node_address  = '192.168.3.9' # CHANGEME

$controller_node_public   = $controller_node_address
$controller_node_internal = $controller_node_address
$sql_connection         = "mysql://nova:${nova_db_password}@${controller_node_internal}/nova"

# this machine
node /moc-node-9/ { # CHANGEME

  ### NEW
  include 'apache'

  class { 'openstack::controller':
    public_address          => $controller_node_public,
    public_interface        => $public_interface,
    private_interface       => $private_interface,
    internal_address        => $controller_node_internal,
    fixed_range             => $fixed_network_range,
    # by default it does not enable multi-host mode
    multi_host              => true,
    # by default is assumes flat dhcp networking mode
    network_manager         => 'nova.network.manager.FlatDHCPManager',
    verbose                 => $verbose,
    auto_assign_floating_ip => $auto_assign_floating_ip,
    mysql_root_password     => $mysql_root_password,
    admin_email             => $admin_email,
    admin_password          => $admin_password,
    keystone_db_password    => $keystone_db_password,
    keystone_admin_token    => $keystone_admin_token,
    glance_db_password      => $glance_db_password,
    glance_user_password    => $glance_user_password,
    nova_db_password        => $nova_db_password,
    nova_user_password      => $nova_user_password,
    rabbit_password         => $rabbit_password,
    rabbit_user             => $rabbit_user,
    #export_resources        => false,
    
    ## ADDED
    secret_key              => $secret_key,
    quantum                 => $havequantum,
    cinder                  => $havecinder,
    cinder_user_password    => $cinder_user_password,
    cinder_db_password      => $cinder_db_password,
  }

  class { 'openstack::auth_file':
    admin_password       => $admin_password,
    keystone_admin_token => $keystone_admin_token,
    controller_node      => $controller_node_internal,
  }


}

# our compute node
node /moc-node-(11|13)/ { # CHANGEME

  class { 'openstack::compute':
    public_interface   => $public_interface,
    private_interface  => $private_interface,
    internal_address   => $ipaddress_eth0,
    libvirt_type       => 'kvm',
    fixed_range        => $fixed_network_range,
    network_manager    => 'nova.network.manager.FlatDHCPManager',
    multi_host         => true,
#    sql_connection     => $sql_connection,
    nova_user_password => $nova_user_password,
    nova_db_password   => $nova_db_password,
#    quantum_user_password => $quantum_user_password,
    rabbit_host        => $controller_node_internal,
    rabbit_password    => $rabbit_password,
    rabbit_user        => $rabbit_user,
    glance_api_servers => "${controller_node_internal}:9292",
    vncproxy_host      => $controller_node_public,
    vnc_enabled        => true,
    verbose            => $verbose,
    manage_volumes     => false,
    volume_group       => 'cinder-volumes',

    quantum                 => $havequantum,
#    cinder                  => $havecinder,

#    cinder_user_password    => $cinder_user_password,
    cinder_db_password      => $cinder_db_password,

    keystone_host      => $controller_node_internal,

    db_host            => $controller_node_internal,    

  }

}

