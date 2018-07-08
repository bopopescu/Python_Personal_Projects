import app_util.db as db
import app_util.constants as const

class ClienteModel():

	def __init__(self, codigo, nome, sobrenome, email, residencial, celular):

		self.codigo = codigo
		self.nome = nome
		self.sobrenome = sobrenome
		self.email = email
		self.residencial = residencial
		self.celular = celular

	@classmethod
	def query_by_id(cls, _id):

		cliente = db.execute_query_with_one_result(CLIENTE_LOJA_BY_ID, _id)

		return cls(cliente[0], cliente[1], cliente[2], cliente[3], 
			cliente[4], cliente[5])

	def insert():

		db.execute_dml(const.INSERT_CEP, self.nome, self.sobrenome, self.email, 
			self.residencial, self.celular)

