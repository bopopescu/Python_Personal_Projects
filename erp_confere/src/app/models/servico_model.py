import app_util.db as db
import app_util.constants as const

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

	def update(self):

		db.execute_dml(const.UPDATE_SERVICO, self.nome, self.valor, 
			self.sequencia, self.tipo_valor_servico, self.codigo)

