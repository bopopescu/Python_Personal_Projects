import app_util.db as db
import app_util.constants as const

class PedidoServicoModel():

	def __init__(self, codigo, pedido, servico, funcionario, data_inicio,
		valor_comissao, data_fim, servico_props):

		self.codigo = codigo 
		self.pedido = pedido
		self.servico = servico
		self.funcionario = funcionario
		self.data_inicio = data_inicio
		self.valor_comissao = valor_comissao
		self.data_fim = data_fim
		self.servico_props = servico_props

	