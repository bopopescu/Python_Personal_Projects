from flask_restful import Resource, request
from models.funcao_model import FuncaoModel

class Funcao(Resource):

	def post(self):
		
		data = request.get_json()
		nova_funcao = FuncaoModel(data['nome'])
		nova_funcao.save_to_db()

