from models.pedido_model import PedidoModel
import cep_service

def insert_pedido(json):



def json_to_model(json):

	numero_pedido = json['numero_pedido']
	ambiente = json['ambiente']
	endereco = json['endereco']
	cliente = json['cliente']
	loja = json['loja']
	pedido_pai = json['pedido_pai'] if 'pedido_pai' in json else None
	valor_pedido = json['valor']
	data_entrada = json['data_entrada']
	data_inicio = json['data_inicio'] if 'data_inicio' in json else None
	data_inicio = json['data_fim'] if 'data_fim' in json else None
	servicos = json['servicos']

	return PedidoModel(None, ambiente, cep, cliente, loja, pedido_pai, numero_pedido,
		valor_pedido, data_entrada, data_inicio, data_fim)
