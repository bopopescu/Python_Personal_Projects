import app_util.db as db
import app_util.constants as const
import MySQLdb as mysql

class ServicoModel():

	def __init__(self, codigo, nome, valor, sequencia, tipo_valor_servico):

		self.codigo = codigo
		self.nome = nome
		self.valor = valor
		self.sequencia = sequencia
		self.tipo_valor_servico = tipo_valor_servico

	@classmethod
	def get_by_id(cls, _id):

		servico = db.query_with_one_result(const.QUERY_SERVICO_BY_ID, _id)

		return cls(servico[0], servico[1], servico[2], servico[3],
				servico[4])

	@classmethod
	def get_in_id(cls, servicos_id):

		servicos_in = ','.join(['%s'] * len(servicos_id))
		conn, cx = db.get_db_resources()

		try:
			cx.execute(const.QUERY_SERVICO_IN_ID % servicos_in, servicos_id)
			# print(cx._last_executed) # Prints the last SQL executed
			servicos = cx.fetchall()
			servicos_object = [cls(servico[0], servico[1], servico[2], 
				servico[3], servico[4])for servico in servicos]
		except mysql.Error as e:
			raise
		else:
			if len(servicos_object) == 0:
				return None

			return servicos_object
		finally:
			conn.close()
			cx.close()

	def update(self):

		db.execute_dml(const.UPDATE_SERVICO, self.nome, self.valor, 
			self.sequencia, self.tipo_valor_servico, self.codigo)
