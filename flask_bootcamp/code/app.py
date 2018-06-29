from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'vinicius'
# Exposed the app to the API class
api = Api(app)


# Creates a new endpoint /auth
jwt = JWT(app, authenticate, identity) 

items = []

# All classes which are going to be exposed as a resource must extend Resource class
class Item(Resource):


	def get(self,name):

		# By returning None we can control the code flow and avoid exceptions
		item = next(list(filter(lambda x: x['name'] == name, items)), None)

		return {'item': item}, 200 if item else 404


	def post(self,name):

		if(next(filter(lambda x: x['name'] == name, items)), None):
			return {'message', "An item with name {} already exists".format(name)}, 400

		# force=True doesn't look at content-type before receiving the request
		# silent=True Doesn't return an error, only None when the format is not correct. 
		request_data = request.get_json(silent=True) 

		item = {'name': name, 'price': request_data['price']}
		items.append(item)
		return item, 201


class ItemList(Resource):
	def get(self):
		return {'items': items}




# Makes the resource accessable 
api.add_resource(Item, '/item/<string:name>') # http://localhost:5000/student/Rolf
api.add_resource(ItemList, '/items')

# Run the app listening at port 5000
# Don't use debug on production environments
app.run(port=5000, debug=True)