import app_util.db as db
import app_util.constants as const
import json
import app_util.json_util as json_util
import services.servico_service as servico_service
import copy
from models.pedido_servico_model import PedidoServicoModel  
from services import funcionario_service
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

	updated_values = validate_from_form(pedido_servico, **kwargs)

	conn, cr = db.get_db_resources()

	try:
		cr.callproc('prc_update_pedido_servico', (updated_values.pedido.codigo, updated_values.servico.codigo, updated_values.funcionario,
			updated_values.valor_comissao, updated_values.data_inicio, updated_values.data_fim, json_util.dict_to_str(updated_values.servico_props)))
	except:
		raise
	else:
		conn.commit()
	finally:
		cr.close()
		conn.close()

def validate_from_form(pedido_servico, **kwargs):

	updated_values = copy.deepcopy(pedido_servico)
	if 'comentario' in kwargs:
		if kwargs['comentario']:
			if 'comentario' in pedido_servico.servico_props:
				if kwargs['comentario'] != pedido_servico.servico_props['comentario']:
					updated_values.servico_props['comentario'] = kwargs['comentario']
			else:
				updated_values.servico_props['comentario'] = kwargs['comentario']	

	if 'funcionario' in kwargs:
		if kwargs['funcionario']:
			if pedido_servico.funcionario:
				if kwargs['funcionario'] != pedido_servico.funcionario.codigo:
					updated_values.funcionario = kwargs['funcionario']
			else:
				updated_values.funcionario = kwargs['funcionario']
		elif not kwargs['funcionario'] and kwargs['status'] == 'novo':
			updated_values.funcionario = None
		else:
			raise ValueError('Não é permitido ficar sem responsável quando já foi iniciado ')

	if 'promob_inicial' in kwargs:
		if kwargs['promob_inicial']:
			if 'promob_inicial' in pedido_servico.servico_props:
				if kwargs['promob_inicial'] != pedido_servico.servico_props['promob_inicial']:
					updated_values.servico_props['promob_inicial']
			else:
				updated_values.servico_props['promob_inicial'] = kwargs['promob_inicial']

	if 'promob_final' in kwargs:
		if kwargs['promob_final']:
			if 'promob_final' in pedido_servico.servico_props:
				if kwargs['promob_final'] != pedido_servico.servico_props['promob_final']:
					updated_values.servico_props['promob_final']
			else:
				updated_values.servico_props['promob_final'] = kwargs['promob_final']

	if 'agendamento' in kwargs:
		if kwargs['agendamento']:
			if 'agendamento' in pedido_servico.servico_props:
				if kwargs['agendamento'] != pedido_servico.servico_props['agendamento'][-1]:
					print(pedido_servico.servico_props['agendamento'])
					updated_values.servico_props['agendamento'][-1] = kwargs['agendamento']
			else:
				updated_values.servico_props['agendamento'] = [kwargs['agendamento']]

	for indx in range(3):
		key_medicao = 'medicao_%s' % indx
		if key_medicao in kwargs:
			if kwargs[key_medicao]:
				if 'agendamento' in pedido_servico.servico_props:
					if kwargs[key_medicao] != pedido_servico.servico_props['agendamento'][indx]:
						print(pedido_servico.servico_props['agendamento'])
						updated_values.servico_props['agendamento'][indx] = kwargs[key_medicao]
				else:
					updated_values.servico_props['agendamento'] = [kwargs[key_medicao]]

	return updated_values
