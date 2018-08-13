import app_util.db as db
import app_util.constants as const

class UsuarioModel(object):

	def __init__(self, codigo, username, password, data_criacao, 
		data_alteracao, funcao):

		self.codigo = codigo
		self.username = username
		self.password = password
		self.data_criacao = data_criacao
		self.data_alteracao = data_alteracao
		self.funcao = funcao

	@classmethod
	def query_by_id(cls, _id):

		sql = None

		if type(_id) == int:
			sql = const.QUERY_USUARIO_BY_ID
		else:
			sql = const.QUERY_USUARIO_BY_USERNAME

		usuario = db.query_with_one_result(sql, _id)

		return cls(usuario[0], usuario[1], usuario[2], usuario[3], 
			usuario[4], usuario[5])

	def insert():

		db.execute_dml(const.INSERT_USUARIO, self.codigo, self.username, self.password, 
			self.password, self.data_criacao, self.data_alteracao, self.funcao)

		