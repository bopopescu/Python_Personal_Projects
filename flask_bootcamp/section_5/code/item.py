import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

class Item(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('price', required=True,type=float,help="This field cannot be left in blank")

	def get(self,name):

		item = self.find_by_name(name)
		if item:
			return item
		
		return {'message': 'Item not found'}, 404

	@classmethod
	def find_by_name(cls, name):
		conn = sqlite3.connect('data.db')
		
		cursor = conn.cursor()

		query = "SELECT * FROM items WHERE name=?"
		result = cursor.execute(query, (name,)) 
		row = result.fetchone()

		conn.close()

		if row:
			return {'item': {'name': row[0], 'price': row[1]}}

	def post(self,name):

		if self.find_by_name(name):
			return {'message': "An item iwth name '{}' already exists".format(name)}, 400

		data = Item.parser.parse_args()
		item = {'name': name, 'price': data['price']}

		conn = sqlite3.connect('data.db')
		cursor = conn.cursor()

		query = "INSERT INTO items VALUES(?,?)"

		cursor.execute(query, (item['name'], item['price']))
		
		conn.commit()
		conn.close()

		return item, 201

	def delete(self, name):

		pass

	def put(self,name):
		
		pass


class ItemList(Resource):
	pass