import app_util.db as db
import app_util.constants as const


class CepModel():

	def __init__(self, cep, logradouro, complemento, bairro, cidade, uf):

		self.cep = cep
		self.logradouro = logradouro
		self.complemento = complemento 
		self.bairro = bairro
		self.cidade = cidade
		self.uf = uf

	@classmethod
	def query_by_id(cls, _id):

		cep = db.query_with_one_result(const.QUERY_CEP_BY_ID, _id)

		return cls(cep[0], cep[1], cep[2], cep[3], cep[4], cep[5])

	def insert(self):

		db.execute_dml(const.INSERT_CEP, self.cep, self.logradouro, self.complemento,self.bairro, 
			self.cidade, self.uf)