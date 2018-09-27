from model.models import Pedido, StatusPedido
import services.cliente_endereco_service as cliente_endereco_service
import services.loja_service as loja_service
import services.servico_service as servico_service
import services.pedido_servico_service as pedido_servico_service
from persistence.mysql_persistence import db
import json
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
	servicos_to_create = servico_service.query_servicos(servicos)
	pedido_servicos = [pedido_servico_service.generate_pedido_servico(pedido, servico) for servico in servicos_to_create]

	insert_pedido_pedido_servico(pedido, pedido_servicos)

	return pedido

def insert_pedido_pedido_servico(pedido, pedido_servicos):
		db.session.add(pedido)
		db.session.add_all(pedido_servicos)
		db.session.commit()
		db.session.close()


def jason_to_model(dic):

	numero_pedido = dic['numero_pedido']
	ambiente = dic['ambientes'] if 'ambientes' in dic else None
	loja = dic['loja']
	pedido_pai = dic['pedido_pai'] if 'pedido_pai' in dic else None
	valor_pedido = dic['valor_pedido']
	data_entrada = dic['data_entrada']
	data_inicio = dic['data_inicio'] if 'data_inicio' in dic else None
	data_fim = dic['data_fim'] if 'data_fim' in dic else None

	cliente_endereco = cliente_endereco_service.cliente_endereco_handler(dic)

	return Pedido(cliente_endereco_obj=cliente_endereco, loja=loja, complemento=pedido_pai, 
		numero=numero_pedido, valor=valor_pedido, data_entrada=data_entrada, data_inicio=data_inicio, data_fim=data_fim, ambientes=ambiente, status=StatusPedido.novo)


def query_pedido_by_id(codigo):
	return Pedido.query.filter_by(codigo=codigo).first()

def query_pedidos():
	return Pedido.query.all()

def compose_pedido(db_row):
	pedido = db_to_model(db_row)
	codigo_cliente_endereco = pedido.cliente_endereco
	
	pedido.cliente_endereco = cliente_endereco_service.get_cliente_endereco(codigo_cliente_endereco)
	pedido.loja = loja_service.query_loja_by_id(pedido.loja)
	return pedido
