import app_util.db as db
import app_util.constants as const

class FuncaoModel(object):

	def __init__(self, codigo, nome):

		self.codigo = codigo
		self.nome = nome

	@classmethod
	def query_by_id(cls, _id):

		funcao = db.query_with_one_result(FUNCAO_LOJA_BY_ID, _id)

		return cls(funcao[0], funcao[1])

	def insert(self):

		db.execute_dml(INSERT_FUNCAO, self.nome)
