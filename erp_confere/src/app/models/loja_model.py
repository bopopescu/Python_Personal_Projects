import app_util.db as db
import app_util.constants as const


class LojaModel():


	def __init__(self, codigo, nome, valor_comissao):
		
		self.codigo = codigo
		self.nome = nome
		self.valor_comissao = valor_comissao

	def get_all():

		QUERY_ALL = "SELECT * FROM lojas" 

		cnx = db.get_connection()

		cur = cnx.cursor()

		cur.execute(QUERY_ALL)

	@classmethod
	def get_by_id(cls, _id):		

		loja = db.query_with_one_result(const.QUERY_LOJA_BY_ID, _id)

		return cls(loja[0], loja[1], loja[2])

	def insert(self):

		db.execute_dml(const.INSERT_LOJA, self.nome, self.valor_comissao)

	def update(self):

		db.execute_dml(const.UPDATE_LOJA, self.nome, self.valor_comissao, self.codigo)