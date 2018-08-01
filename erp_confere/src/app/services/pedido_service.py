from models.pedido_model import PedidoModel
import services.cliente_endereco_service as cliente_endereco_service
import services.loja_service as loja_service
import services.servico_service as servico_service
import services.pedido_servico_service as pedido_servico_service

import json

import app_util.db as db
import app_util.constants as const

# def create_pedido_handler(jason):

# 	pedido = jason_to_model(jason)
# 	servicos = jason['servicos'] if 'servicos' in jason else None
# 	servicos_to_create = servico_service.get_servicos(servicos)
# 	pedido_servicos = [pedido_servico_service.json_to_model(pedido, servico) for servico in servicos_to_create]

# 	insert_pedido(pedido, pedido_servicos)

# 	return pedido

def create_pedido_handler(dic):
		
	pedido = jason_to_model(dic)
	servicos = dic['servicos'] if 'servicos' in dic else None
	servicos_to_create = servico_service.get_servicos(servicos)
	pedido_servicos = [pedido_servico_service.generate_pedido_servico(pedido, servico) for servico in servicos_to_create]

	insert_pedido(pedido, pedido_servicos)

	return pedido

def insert_pedido(pedido, pedido_servicos):

	conn, cursor = db.get_db_resources()
	
	print(pedido.ambiente)

	try:
		pedido_props = (pedido.codigo, pedido.cep.cep, pedido.cliente.codigo, pedido.loja.codigo, 
				pedido.pedido_pai, pedido.numero_pedido, pedido.valor_pedido, pedido.data_entrada, 
				pedido.data_inicio, pedido.data_fim, pedido.ambiente)	
		cursor.callproc('prc_insert_pedido', pedido_props)
		cursor.execute('SELECT @_prc_insert_pedido_0')
		pedido.codigo = cursor.fetchone()[0]

		for pedido_servico in pedido_servicos:

			pedido_servico_props = (pedido.codigo, pedido_servico.servico.codigo, pedido_servico.funcionario, 
				pedido_servico.valor_comissao, pedido_servico.data_inicio, pedido_servico.data_fim,
				pedido_servico.servico_props)
			cursor.callproc("prc_insert_pedido_servico", pedido_servico_props)
	except:
		raise
	else:
		conn.commit()
	finally:
		cursor.close()
		conn.close()

def jason_to_model(dic):

	numero_pedido = dic['numero_pedido']
	ambiente = json.dumps(dic['ambientes']) if 'ambientes' in dic else None
	loja = dic['loja']
	pedido_pai = dic['pedido_pai'] if 'pedido_pai' in dic else None
	valor_pedido = dic['valor_pedido']
	data_entrada = dic['data_entrada']
	data_inicio = dic['data_inicio'] if 'data_inicio' in dic else None
	data_fim = dic['data_fim'] if 'data_fim' in dic else None

	loja = loja_service.query_loja(loja)
	cliente_endereco = cliente_endereco_service.cliente_endereco_handler(dic)

	return PedidoModel(None, cliente_endereco.cep, cliente_endereco.cliente, loja, pedido_pai, 
		numero_pedido, valor_pedido, data_entrada, data_inicio, data_fim, ambiente)
