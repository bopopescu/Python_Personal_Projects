import app_util.db as db
import app_util.constants as const

class ClienteModel(object):

	def __init__(self, codigo, nome, sobrenome, email, residencial, celular):

		self.codigo = codigo
		self.nome = nome
		self.sobrenome = sobrenome
		self.email = email
		self.residencial = residencial
		self.celular = celular

	@classmethod
	def query_by_id(cls, _id):
		cliente = db.query_with_one_result(const.CLIENTE_BY_ID, _id)

		if cliente: 
			return cls(cliente[0], cliente[1], cliente[2], cliente[3],
				cliente[4], cliente[5])
		return None

	def insert(self):

		insert_id = db.execute_dml(const.INSERT_CLIENTE, self.nome, self.sobrenome, self.email, 
			self.residencial, self.celular)

		self.codigo = insert_id

	@classmethod
	def query_by_name(cls, nome, sobrenome):
		cliente = db.query_with_one_result(const.CLIENTE_BY_NOME, nome, sobrenome)

		if cliente: 
			return cls(cliente[0],cliente[1], cliente[2], cliente[3],
				cliente[4], cliente[5])

		return None