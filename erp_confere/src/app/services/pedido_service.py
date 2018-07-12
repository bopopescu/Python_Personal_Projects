from models.pedido_model import PedidoModel
import services.cliente_endereco_service as cliente_endereco_service
import json
import services.loja_service as loja_service

def insert_pedido(jason):

	pedido = jason_to_model(jason)

	if pedido:
		pedido.insert()

	return pedido


def jason_to_model(jason):

	numero_pedido = jason['numero']
	ambiente = json.dumps(jason['ambiente']) if 'ambiente' in jason else None 
	endereco = jason['endereco']
	cliente = jason['cliente']
	loja = jason['loja']
	pedido_pai = jason['pedido_pai'] if 'pedido_pai' in jason else None
	valor_pedido = jason['valor']
	data_entrada = jason['data_entrada']
	data_inicio = jason['data_inicio'] if 'data_inicio' in jason else None
	data_fim = jason['data_fim'] if 'data_fim' in jason else None
	servicos = jason['servicos']

	loja = loja_service.query_loja(loja)
	
	cliente_endereco = cliente_endereco_service.cliente_endereco_service(jason)

	return PedidoModel(None, cliente_endereco.cep, cliente_endereco.cliente, loja, pedido_pai, 
		numero_pedido, valor_pedido, data_entrada, data_inicio, data_fim, ambiente)
