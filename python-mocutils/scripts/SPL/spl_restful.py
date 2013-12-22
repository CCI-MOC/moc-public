
from flask import Flask, jsonify, abort, make_response, request
import spl_control
import spl_er
import spl_config

app = Flask(__name__)



'''

GET
/groups
/groups/group_name

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

'''
get_groups()

1. query the database from Group
2. get a list of groups
2. jsonify the list



'''


groups = [
    {
        'group_name': 'group1',
        'vm_name': 'vm1',
        'network_id': 101, 
        'deployed': True
    },
    {
        'group_name': 'group2',
        'vm_name': 'vm2',
        'network_id': 102, 
        'deployed': True
    }
]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/groups', methods = ['GET'])
def get_groups():
    query_db(Group)
    return jsonify( { 'groups': groups } )

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


@app.route('/groups/<group_name>', methods = ['PUT'])
def update_group(group_name):
    group = filter(lambda g: g['group_name'] == group_name, groups)
    if len(group) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'vm_name' in request.json and type(request.json['vm_name']) is not unicode:
        abort(400)
    if 'network_id' in request.json and type(request.json['network_id']) is not int:
        abort(400)
    if 'deployed' in request.json and type(request.json['deployed']) is not bool:
        abort(400)
    group[0]['vm_name'] = request.json.get('vm_name',group[0]['vm_name'])
    group[0]['network_id'] = request.json.get('network_id',group[0]['network_id'])
    group[0]['deployed'] = request.json.get('deployed',group[0]['deployed'])
    return jsonify( { 'group':group[0]})

@app.route('/groups/<group_name>', methods = ['DELETE'])
def delete_group(group_name):
    group = filter(lambda g: g['group_name'] == group_name, groups)
    if len(group) == 0:
        abort(404)
    groups.remove(group[0])
    return jsonify( { 'result':True })

    


if __name__ == '__main__':
    app.run(debug = True)
