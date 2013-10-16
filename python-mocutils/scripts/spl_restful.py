from flask import Flask
from flask.ext import restful

app = Flask(__name__)
api = restful.Api(app)


#The class is a resource
class Group(restful.Resource):
    def get(self):
        return {
	"group_name": "group1",
	"vm_name": "vm1",
	"network_id": 101,
	"nodes": [ 1,2,3]
}


api.add_resource(Group, '/')

if __name__ == '__main__':
    app.run(debug=True)
    
