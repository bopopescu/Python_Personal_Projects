import app_util.db as db
import app_util.constants as const

class Pedido():

	def __init__(self, codigo, ambiente, cep, cliente, loja, pedido_pai, 
		numero_pedido, valor_pedido, data_entrada, data_inicio, data_fim):

		self.codigo = codigo
		self.ambiente = ambiente
		self.cep = cep
		self.cliente = cliente
		self.loja = loja
		self.pedido_pai = pedido_pai
		self.numero_pedido
		self.valor_pedido = valor_pedido
		self.data_entrada = data_entrada
		self.data_inicio = data_inicio
		self.data_fim = data_fim

