import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel 


class UserRegister(Resource):

	parser = reqparse.RequestParser()

	parser.add_argument('username', required=True,type=str,help='Username to be persisted')
	parser.add_argument('password', required=True,type=str,help='Username to be persisted')

	def post(self):
		data = UserRegister.parser.parse_args()
		user = UserModel.find_by_username(data['username'])

		if user:
			return {"message": "User '{}' already exists".format(data['username']) }, 400

		user = UserModel(**data)
		user.save_to_db()

		return {"message": "User created successfully"}, 201
























