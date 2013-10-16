# This module allows for an openstack deployment with one control node, assuming the
# network setup used with the mocpoc. Here is a sample site.pp, which should
# be sufficient:
#
# class { 'mocpoc':
#	moc_password => 'changeme',
#	controller_node => '192.168.3.123',
# }
#
# This sets up a cluster with a control node on the machine with the specified
# ip. Any other puppet agents will become compute nodes. the password
# 'changeme' will be used for most services.

# required variables:
# [moc_password] - default service password
# [controller_node] - public ip of the machine to be configured as a controller.
# other configurable variables:
class mocpoc (
	$moc_password,
	$controller_node,
) {

  $admin_email = 'root@localhost'
  $rabbit_user = 'openstack_rabbit_user'
  $fixed_network_range = '192.168.15.0/24'
  $verbose = false
  $auto_assign_floating_ip = false
  $havecinder = false
  $havequantum  = false

  $ipaddress_public = $ipaddress_eth1
  $ipaddress_private = $ipaddress_eth0
  $public_interface = 'eth1'
  $private_interface = 'eth0'

  $mysql_root_password = $moc_password
  $admin_password = $moc_password
  $keystone_admin_token = $moc_password
  $keystone_db_password = $moc_password
  $glance_db_password = $moc_password
  $glance_user_password = $moc_password
  $nova_db_password = $moc_password
  $nova_user_password = $moc_password
  $pasword = $moc_password

  $quantum = $havequantum
  $cinder = $havecinder
  $cinder_user_password = $moc_password
  $cinder_db_password = $moc_password

  $controller_node_public   = $controller_node
  $controller_node_internal = $controller_node
  

  # deploy a script that can be used to test nova
  class { 'openstack::test_file': }

  if $ipaddress_public == $controller_node {
    class { 'openstack::controller':
      public_address          => $controller_node_public,
      public_interface        => $public_interface,
      private_interface       => $private_interface, 
      internal_address        => $ipaddress_public,
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
  } else {
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

}

# vim:set ts=2 sw=2 et:

