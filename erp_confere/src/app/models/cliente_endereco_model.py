import app_util.db as db
import app_util.constants as const

class ClienteEnderecoModel():

	def __init__(self, cep, cliente, numero_endereco, complemento,
		referencia):

		self.cep = cep
		self.cliente = cliente
		self.numero_endereco = numero_endereco
		self.complemento = complemento
		self.referencia = referencia

	def insert(self):

		db.execute_dml(const.INSERT_CLIENTE_ENDERECO, self.cep.cep, self.cliente.codigo, self.numero_endereco,
			self.complemento, self.referencia)

	@classmethod
	def query_by_id(cls, cep, codigo_cliente):

		cliente_endereco = db.query_with_one_result(const.SELECT_CLIENTE_ENDERECO, cep, codigo_cliente)

		if cliente_endereco:
			return cls(cliente_endereco[0], cliente_endereco[1], cliente_endereco[2], cliente_endereco[3],
				cliente_endereco[4])

		return None