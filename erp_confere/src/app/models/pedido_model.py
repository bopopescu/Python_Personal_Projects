import app_util.db as db
import app_util.constants as const

class PedidoModel():

	def __init__(self, codigo, cep, cliente, loja, pedido_pai, numero_pedido, 
		valor_pedido, data_entrada, data_inicio, data_fim, ambiente):

		self.codigo = codigo
		self.cep = cep
		self.cliente = cliente
		self.loja = loja
		self.pedido_pai = pedido_pai
		self.numero_pedido = numero_pedido
		self.valor_pedido = valor_pedido
		self.data_entrada = data_entrada
		self.data_inicio = data_inicio
		self.data_fim = data_fim
		self.ambiente = ambiente

	def insert(self):

		db.execute_dml(const.INSERT_PEDIDO, self.codigo, self.cep.cep, self.cliente.codigo, self.loja.codigo, 
			self.pedido_pai, self.numero_pedido, self.valor_pedido, self.data_entrada, 
			self.data_inicio, self.data_fim, self.ambiente)
