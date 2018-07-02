from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('price', required=True,type=float,help="This field cannot be left in blank")
	parser.add_argument('store_id', required=True,type=int,help="Stoer id")

	def get(self,name):

		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		
		return {'message': 'Item not found'}, 404

	def post(self,name):

		if ItemModel.find_by_name(name):
			return {'message': "An item iwth name '{}' already exists".format(name)}, 400

		data = Item.parser.parse_args()
		item = ItemModel(name, **data)

		try:
			item.save_to_db()
		except:
			return {'message': 'An error ocurred inserting the item.'}, 500

		return item.json(), 201

	def delete(self, name):
		item = Item.find_by_name(name)
		if item:
			item.delete_from_db()

		return {'message': 'Item deleted'}

		
	def put(self,name):
		
		data = Item.parser.parse_args()

		item = ItemModel.find_by_name(name)
		
		try:
			if item is None:
				item = ItemModel(name, **data)
			else:
				item.price = data['price']

			item.save_to_db()
		except: 
			return {'message': 'Error while updating the item'}, 500

		return item.json()

class ItemList(Resource):
	
	def get(self):
		{'items': [item.json() for item in ItemModel.query.all()]}