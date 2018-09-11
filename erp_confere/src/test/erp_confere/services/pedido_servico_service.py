import app_util.constants as const
import json
import app_util.json_util as json_util
import services.servico_service as servico_service
import copy
import datetime
import contextlib
from model.models import PedidoServico  
from services import funcionario_service
from services import pedido_service
from persistence.mysql_persistence import db

def json_to_model(pedido, servico):
	status = json_util.dict_to_str({'status': 'novo'})
	return PedidoServicoModel(pedido, servico, None, 0, None, None, status)	

def generate_pedido_servico(pedido, servico):
	status = json_util.dict_to_str({'status': 'novo'})
	return PedidoServicoModel(pedido, servico, None, 0, None, None, status)	

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
	return PedidoServico.query.filter_by(pedido=codigo_pedido).all()


def get_pedido_servico_by_servico(codigo_pedido):

	pedido_servicos = query_pedido_servico_by_pedido(codigo_pedido)
	for pedido_servico in pedido_servicos:
		pedido_servico.servico = servico_service.query_servico_by_id(pedido_servico.servico)
		pedido_servico.funcionario = funcionario_service.query_funcionario_by_id(pedido_servico.funcionario)

	return pedido_servicos

def get_pedido_servico_by_pedido_servico(codigo_pedido, codigo_servico):
	return PedidoServico.query.filter_by(pedido=codigo_pedido, servico=codigo_servico)


def update_pedido_servico(**kwargs):
	pedido_servico = get_pedido_servico_by_pedido_servico(kwargs['codigo_pedido'], kwargs['codigo_servico'])
	updated_values = validate_from_form(pedido_servico, **kwargs)
	update_model(updated_values)


def update_model(pedido_servico):
	if not pedido_servico:
		raise ValueError('Pedido serviço não pode ser nulo')
	if not pedido_servico.pedido:
		raise ValueError('Pedido não pode ser nulo')
	if not pedido_servico.servico:
		raise ValueError('Serviço não pode ser nulo')
	if not pedido_servico.funcionario:
		funcionario = None
	else:
		funcionario = pedido_servico.funcionario.codigo

	try:
		conn, cr = db.get_db_resources()
		cr.callproc('prc_update_pedido_servico', (pedido_servico.pedido.codigo, pedido_servico.servico.codigo, funcionario,
			pedido_servico.valor_comissao, pedido_servico.data_inicio, pedido_servico.data_fim, json_util.dict_to_str(pedido_servico.servico_props)))
	except:
		raise
	else:
		conn.commit()
	finally:
		cr.close()
		conn.close()


def agendar_iniciar(**kwargs):
	'''
		Update pedido_servico's status
		Novo -> Agendado/Iniciado -> Concluído -> Liberado
		Medição/Atendimento:
			data agendamento
			funcionario
		Subir Paredes/ Projeto / Liberação / Manual de montagem:
			funcinoario
	'''
	print(kwargs)
	if kwargs['status'] == 'novo':
		if kwargs['funcionario']:
			pedido_servico = get_pedido_servico_by_pedido_servico(kwargs['codigo_pedido'], kwargs['codigo_servico'])
			pedido_serivco_changeable = is_pedido_servico_status_changeable(pedido_servico)
			
			if pedido_serivco_changeable:
				updated_pedido_servico = validate_from_form(pedido_servico, **kwargs)
				
				is_medicao_or_atendimento = kwargs['nome_servico'] == 'medicao' or kwargs['nome_servico'] == 'atendimento'
				if is_medicao_or_atendimento:
					if 'medicao_0' in kwargs or 'agendamento' in kwargs:
						updated_pedido_servico.servico_props['status'] = 'agendado'
					else:
						raise ValueError('Favor informar a data de agendamento')
				else:
					updated_pedido_servico.servico_props['status'] = 'iniciado'

				updated_pedido_servico.servico_props['status'] = 'iniciado'
				updated_pedido_servico.data_inicio = datetime.date.today()
				update_model(updated_pedido_servico)
			else:
				raise ValueError('Favor encerrar devidamente o serviço anterior')
		else:
			raise ValueError('Favor informar o funcionario')
	else:
		raise ValueError('Pedido foi solicitado o agendamento/inicialização, porém não está aberto')


def concluir(**kwargs):
	pedido_servico = get_pedido_servico_by_pedido_servico(kwargs['codigo_pedido'], kwargs['codigo_servico'])
	pedido_serivco_changeable = is_pedido_servico_status_changeable(pedido_servico)

	if pedido_serivco_changeable:
		if validate_pedido_servico(**kwargs):
			updated_pedido_servico = validate_from_form(pedido_servico, **kwargs)
			updated_pedido_servico.servico_props['status'] = 'concluido'
			updated_pedido_servico.data_fim = datetime.date.today()
			update_model(updated_pedido_servico)
		else:
			raise ValueError('Não há informações para tratar')
	else:
		raise ValueError('Favor encerrar devidamente o serviço anterior')

def reabrir(**kwargs):
	nome_servico = kwargs['nome_servico']
	current_status = kwargs['status']
	pedido_servico = get_pedido_servico_by_pedido_servico(kwargs['codigo_pedido'], kwargs['codigo_servico'])

	if current_status == 'concluido':
		if nome_servico == 'medicao' or nome_servico == 'atendimento':
			pedido_servico.servico_props['status'] = 'agendado'
		else:
			pedido_servico.servico_props['status'] = 'iniciado'
		update_model(pedido_servico)


def validate_pedido_servico(**kwargs):
	nome_servico = kwargs['nome_servico']
	if nome_servico == 'medicao' or nome_servico == 'atendimento':
		return validate_agendamento(**kwargs)
	elif nome_servico == 'subir_paredes' or nome_servico == 'liberacao':
		return validate_promob(**kwargs)
	elif nome_servico == 'projeto' or nome_servico == 'manual_de_montagem':
		return True
	else:
		return False


def validate_promob(**kwargs):
	return 'promob_inicial' in kwargs or 'promob_final' in kwargs


def validate_agendamento(**kwargs):
	if 'agendamento' in kwargs:
		return True
	for indx in range(3):
		nome_kwargs = 'medicao_' + str(indx)
		if nome_kwargs in kwargs:
			return True
	return False

def is_pedido_servico_status_changeable(pedido_servico):
	previous_state = None
	try:
		conn = db.get_db_connection()
		with contextlib.closing(conn.cursor()) as cnx:
			cnx.callproc('prc_get_previous_status_pedido_servico', (pedido_servico.pedido.codigo, 
				pedido_servico.servico.codigo, previous_state))
			cnx.execute('SELECT @_prc_get_previous_status_pedido_servico_2')
			previous_state = cnx.fetchone()[0]
	except:
		raise
	else:
		conn.close()

	is_changeable = previous_state == 'concluido' or previous_state == 'liberado' or not previous_state
	if is_changeable:
		return True
	return False



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
					updated_values.funcionario = funcionario_service.query_funcionario_by_id(kwargs['funcionario'])
			else:
				updated_values.funcionario = funcionario_service.query_funcionario_by_id(kwargs['funcionario'])
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
				print(pedido_servico.servico_props['agendamento'])
				updated_values.servico_props['agendamento'].append(kwargs['agendamento'])
				print(kwargs['agendamento'])
				print(updated_values.servico_props['agendamento'])
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
