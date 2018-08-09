import app_util.db as db
import app_util.constants as const
from models.pedido_servico_model import PedidoServicoModel  
import app_util.json_util as json_util
import services.servico_service as servico_service
from services import funcionario_service
import json

def insert_pedido_servico(pedido_servico):
	pass


def json_to_model(pedido, servico):

	status = json_util.dict_to_str({'status': 'novo'})

	return PedidoServicoModel(pedido, servico, None, None, 0, None, status)

def generate_pedido_servico(pedido, servico):
	
	status = json_util.dict_to_str({'status': 'novo'})

	return PedidoServicoModel(pedido, servico, None, None, 0, None, status)	


def update_pedido_servico(pedido_servico):

	conn, cr = db.get_db_resources()

	props = json_util.dict_to_str(pedido_servico['props'])

	cr.execute('call prc_update_pedido_servico(%s, %s, %s, %s, %s, %s)', 
		(pedido_servico['codigo'], pedido_servico['funcionario']['codigo'], 
		pedido_servico['valor_comissao'], pedido_servico['data_inicio'], pedido_servico['data_fim'],
		props))

	conn.commit()

	conn.close()

def query_pedido_servico_by_pedido(codigo_pedido):

	conn, cr = db.get_db_resources()

	try:
		cr.callproc('prc_get_pedido_servico_by_pedido', (codigo_pedido, ))
	except:
		raise
	else:
		db_rows = cr.fetchall()
		pedido_servicos = [PedidoServicoModel(db_row[0],db_row[1],db_row[2],db_row[3],db_row[4],db_row[5],
			json.loads(db_row[6])) for db_row in db_rows]
	finally:
		cr.close()
		conn.close()

	return pedido_servicos


def get_pedido_servico_by_servico(codigo_pedido):

	pedido_servicos = query_pedido_servico_by_pedido(codigo_pedido)

	for pedido_servico in pedido_servicos:
		pedido_servico.servico = servico_service.query_servico_by_id(pedido_servico.servico)
		pedido_servico.funcionario = funcionario_service.query_funcionario_by_id(pedido_servico.funcionario)


	return pedido_servicos