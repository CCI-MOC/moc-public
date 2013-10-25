from spl_control import *

load_resources()
query_db(Node)
query_db(VM)
query_db(Network)
create_group("group1","vm1",101)
query_db(Group)
add_node_to_group(1,"group1")
add_node_to_group(2,"group1")
add_node_to_group(3,"group1")
deploy_group("group1")
query_db(Group)
