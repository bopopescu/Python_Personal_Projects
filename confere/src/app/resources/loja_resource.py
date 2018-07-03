from flask_restful import Resource, request
from models.loja_model import LojaModel

class Loja(Resource):

	def get(self,_id):
		return LojaModel.find_by_id(_id)

	def post(self):

		data = request.get_json()

		nova_loja = LojaModel(data['nome'], data['comissao'])

		nova_loja.save_to_db()
