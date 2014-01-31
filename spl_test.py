import spl.control

spl.control.create_node(2)
spl.control.create_node(3)
spl.control.create_node(4)


spl.control.create_nic(2,'mac2','pxe')
spl.control.create_nic(3,'mac3','pxe')
spl.control.create_nic(4,'mac4','pxe')

spl.control.add_nic(2,2)
spl.control.add_nic(3,3)
spl.control.add_nic(4,4)

spl.control.create_switch(1,'dell')

spl.control.create_port(2,1,2)
spl.control.create_port(3,1,3)
spl.control.create_port(4,1,4)

spl.control.connect_nic(2,2)
spl.control.connect_nic(3,3)
spl.control.connect_nic(4,4)


