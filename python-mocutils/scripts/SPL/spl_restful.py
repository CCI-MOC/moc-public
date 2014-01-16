
from flask import Flask, jsonify, abort, make_response, request
import spl_control
import spl_er
import spl_config
from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

app = Flask(__name__)



'''

GET
/groups
/groups/group_name
/groups/group_name/nodes
404 

POST
curl -i -H "Content-Type: application/json" 
 -X POST -d '{"group_name":"group3","vm_name":"vm3","network_id":103}'
  http://localhost:5000/groups

PUT
curl -i -H "Content-Type: application/json" 
 -X PUT -d '{"network_id":600}' 
 http://localhost:5000/groups/group1

DELETE
 curl -i -X DELETE http://localhost:5000/groups/group1

'''


class G():
    pass
g=G()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@auth.verify_password
def verify_password(username, password):
    g.username=username
    return True

@app.route('/groups', methods = ['GET'])
@auth.login_required
def get_groups():
    print g.username
    groups = []
    for group in  spl_control.query_db(spl_er.Group):
        print group
        groups.append({
                'group_name':group.group_name,
                'vm_name':group.vm_name,
                'network_id':group.network_id,
                'deployed':group.deployed
                })

    return jsonify({'groups': groups} )

@app.route('/groups/<group_name>', methods = ['GET'])
def get_group(group_name):
    group = spl_control.get_entity_by_cond(spl_er.Group,"group_name=='%s'"%group_name)
    
    group_dict ={
        'group_name': group.group_name,
        'vm_name': group.vm_name,
        'network_id': group.network_id,
        'deployed': group.deployed,
        }
    return jsonify(group_dict)
 
@app.route('/groups/<group_name>/nodes', methods = ['GET'])
def get_group_nodes(group_name):
    group = spl_control.get_entity_by_cond(spl_er.Group,"group_name=='%s'"%group_name)
    nodes = []
    print group
    for node in group.nodes:
        print node
        nodes.append(node.node_id)
    nodes_dict={"nodes":nodes}
    return jsonify(nodes_dict)

@app.route('/groups/<group_name>/nodes/add/<node_id>',methods = ['GET'])
def add_node_to_group(group_name,node_id):
    node_id = int(node_id)
    group = spl_control.get_entity_by_cond(spl_er.Group,'group_name == "%s"'%group_name)
    node = spl_control.get_entity_by_cond(spl_er.Node, 'node_id == %d'%node_id)
    if not group or not node or node.available == False:
        abort(400)
    node.group = group
    return get_group_nodes(group_name)
    
@app.route('/groups/<group_name>/nodes/remove/<node_id>',methods = ['GET'])
def remove_node_from_group(group_name,node_id):
    node_id = int(node_id)
    group = spl_control.get_entity_by_cond(spl_er.Group,'group_name == "%s"'%group_name)
    node = spl_control.get_entity_by_cond(spl_er.Node, 'node_id == %d'%node_id)
    if not group or not node:
        abort(400)
    node.group = None
    node.available = True
    return get_group_nodes(group_name)



@app.route('/groups', methods = ['POST'])
def create_group():
    if not request.json or not 'group_name' in request.json:
        abort(400)
    group = {
        'group_name': request.json['group_name'],
        'vm_name': request.json['vm_name'],
        'network_id' : request.json['network_id'],
        'deployed' : False
    }
    print group
    spl_control.create_group(group['group_name'],group['vm_name'],group['network_id'])
    groups.append(group)
    return jsonify({ 'group':group}), 201





if __name__ == '__main__':
    app.run(debug = True)
    
 
