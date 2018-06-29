import sqlite3
from flask_restful import Resource, reqparse


class User():

	def __init__(self, _id, username, password):
		self.id = _id
		self.username = username
		self.password = password

	@classmethod
	def find_by_username(cls, username):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = "SELECT * FROM users WHERE username=?"

		# To identify as a tuple with a single value 
		result = cursor.execute(query, (username,))
		row = result.fetchone()
		if row:
			user = cls(*row)
		else:
			user = None 

		connection.close()

		return user

	@classmethod
	def find_by_id(cls, _id):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = "SELECT * FROM users WHERE id=?"

		# To identify as a tuple with a single value 
		result = cursor.execute(query, (_id,))
		row = result.fetchone()
		if row:
			user = cls(*row)
		else:
			user = None 

		connection.close()

		return user

class UserRegister(Resource):

	parser = reqparse.RequestParser()

	parser.add_argument('username', required=True,type=str,help='Username to be persisted')
	parser.add_argument('password', required=True,type=str,help='Username to be persisted')

	def post(self):
		
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		data = UserRegister.parser.parse_args()

		if User.find_by_username(data['username']):
			return {"message": "User '{}' already exists".format(data['username']) }, 400		

		query = "INSERT INTO users VALUES(NULL, ?, ?)"

		cursor.execute(query, (data['username'], data['password']))

		connection.commit()
		connection.close()

		return {"message": "User created successfully"}, 201
























