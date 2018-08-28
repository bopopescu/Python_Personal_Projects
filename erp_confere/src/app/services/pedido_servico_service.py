import app_util.db as db
import app_util.constants as const
from models.pedido_servico_model import PedidoServicoModel  
import app_util.json_util as json_util
import services.servico_service as servico_service
from services import funcionario_service
import json
from services import pedido_service

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

def get_pedido_servico_by_pedido_servico(codigo_pedido, codigo_servico):

	pedido = pedido_service.query_pedido_by_id(codigo_pedido)

	servico = servico_service.query_servico_by_id(codigo_servico)

	conn, cr = db.get_db_resources()
	try:
		cr.callproc('prc_get_pedido_servico_by_id', (codigo_pedido, codigo_servico))
	except:
		raise
	else:
		row = cr.fetchone()
	finally:
		cr.close()
		conn.close()

	pedido_servico = PedidoServicoModel(pedido, servico, row[2], row[3], row[4], row[5], json.loads(row[6]))

	pedido_servico.funcionario = funcionario_service.query_funcionario_by_id(pedido_servico.funcionario)

	return pedido_servico


def update_pedido_servico(**kwargs):

	pedido_servico = get_pedido_servico_by_pedido_servico(kwargs['codigo_pedido'], kwargs['codigo_servico'])

	if kwargs['comentario']:
		if 'comentario' in pedido_servico.servico_props:
			if kwargs['comentario'] != pedido_servico.servico_props['comentario']:
				pedido_servico.servico_props['comentario'] = kwargs['comentario']
		else:
			pedido_servico.servico_props['comentario'] = kwargs['comentario']	

	if kwargs['funcionario']:
		if pedido_servico.funcionario:
			if kwargs['funcionario'] != pedido_servico.funcionario.codigo:
				pedido_servico.funcionario.codigo
		else:
			pedido_servico.funcionario = kwargs['funcionario']

	if kwargs['promob_inicial']:
		if 'promob_inicial' in pedido_servico.servico_props:
			if kwargs['promob_inicial'] != pedido_servico.servico_props['promob_inicial']:
				pedido_servico.servico_props['promob_inicial']
		else:
			pedido_servico.servico_props['promob_inicial'] = kwargs['promob_inicial']

	if kwargs['promob_final']:
		if 'promob_final' in pedido_servico.servico_props:
			if kwargs['promob_final'] != pedido_servico.servico_props['promob_final']:
				pedido_servico.servico_props['promob_final']
		else:
			pedido_servico.servico_props['promob_final'] = kwargs['promob_final']

	if kwargs['agendamento']:
		if ''


