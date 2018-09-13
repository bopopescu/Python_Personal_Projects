import app_util.constants as const
import json
import app_util.json_util as json_util
import services.servico_service as servico_service
import copy
import datetime
import contextlib
from model.models import PedidoServico, Servico 
from services import funcionario_service
from services import pedido_service
from persistence.mysql_persistence import db
from sqlalchemy.orm.exc import NoResultFound

def json_to_model(pedido, servico):
	status = json_util.dict_to_str({'status': 'novo'})
	return PedidoServicoModel(pedido, servico, None, 0, None, None, status)	

def generate_pedido_servico(pedido, servico):
	status = {'status': 'novo'}
	return PedidoServico(pedido_obj=pedido, servico_obj=servico, funcionario_obj=None, 
		valor_comissao=0, data_inicio=None, data_fim=None, servico_props=status)	

def query_pedido_servico_by_pedido(codigo_pedido):
	return PedidoServico.query.filter_by(pedido=codigo_pedido).all()

def query_pedido_servico_by_servico(codigo_pedido):
	pedido_servicos = query_pedido_servico_by_pedido(codigo_pedido)
	return pedido_servicos

def query_pedido_servico_by_pedido_servico(codigo_pedido, codigo_servico):
	return PedidoServico.query.filter_by(pedido=codigo_pedido, servico=codigo_servico).one()

def query_partial_pedido_servico_by_pedido(codigo_pedido):
	result_set = (db.session.query(PedidoServico, Servico).join(PedidoServico.servico_obj) \
		.with_entities(PedidoServico.pedido, PedidoServico.servico, Servico.nome_real, PedidoServico.servico_props) \
		.filter(PedidoServico.pedido == codigo_pedido).all())

	retorno = []
	for row in result_set:
		linha = {}
		linha['pedido'] = row[0]
		linha['servico'] = row[1]
		linha['nome'] = row[2]
		linha['servico_props'] = row[3]
		retorno.append(linha) 

	db.session.close()
	return retorno

def atualiza(**kwargs):
	pedido_servico = query_pedido_servico_by_pedido_servico(kwargs['codigo_pedido'], kwargs['codigo_servico'])
	updated_values = validate_from_form(pedido_servico, **kwargs)
	update_pedido_servico(updated_values)

def update_pedido_servico(pedido_servico):
	if not pedido_servico:
		raise ValueError('Pedido serviço não pode ser nulo')
	if not pedido_servico.pedido:
		raise ValueError('Pedido não pode ser nulo')
	if not pedido_servico.servico:
		raise ValueError('Serviço não pode ser nulo')
	if not pedido_servico.funcionario_obj:
		funcionario_obj = None
	else:
		funcionario_obj = pedido_servico.funcionario_obj

	db.session.commit()

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
			pedido_servico = query_pedido_servico_by_pedido_servico(kwargs['codigo_pedido'], kwargs['codigo_servico'])
			pedido_serivco_changeable = is_pedido_servico_status_changeable(pedido_servico)
			
			if pedido_serivco_changeable:
				# updated_pedido_servico = validate_from_form(pedido_servico, **kwargs)
				validate_from_form(pedido_servico, **kwargs)
				
				is_medicao_or_atendimento = kwargs['nome_servico'] == 'medicao' or kwargs['nome_servico'] == 'atendimento'
				if is_medicao_or_atendimento:
					if 'medicao_0' in kwargs or 'agendamento' in kwargs:
						pedido_servico.servico_props['status'] = 'agendado'
					else:
						raise ValueError('Favor informar a data de agendamento')
				else:
					pedido_servico.servico_props['status'] = 'iniciado'

				pedido_servico.servico_props['status'] = 'iniciado'
				pedido_servico.data_inicio = datetime.date.today()
				update_pedido_servico(pedido_servico)
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
			update_pedido_servico(updated_pedido_servico)
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
		update_pedido_servico(pedido_servico)


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
		previous_state = db.session.query(PedidoServico, Servico)\
			.join(PedidoServico.servico_obj)\
			.with_entities(PedidoServico.servico_props['status'])\
			.filter(PedidoServico.pedido == pedido_servico.pedido, PedidoServico.servico < pedido_servico.servico)\
			.order_by(Servico.sequencia)\
			.limit(1)\
			.one()[0]
	except NoResultFound as e:
		previous_state = None

	print(previous_state)
	is_changeable = previous_state == 'concluido' or previous_state == 'liberado' or not previous_state
	if is_changeable:
		return True
	return False


def validate_from_form(pedido_servico, **kwargs):

	# updated_values = copy.deepcopy(pedido_servico)
	pedido_servico
	if 'comentario' in kwargs:
		if kwargs['comentario']:
			if 'comentario' in pedido_servico.servico_props:
				if kwargs['comentario'] != pedido_servico.servico_props['comentario']:
					pedido_servico.servico_props['comentario'] = kwargs['comentario']
			else:
				pedido_servico.servico_props['comentario'] = kwargs['comentario']	

	if 'funcionario' in kwargs:
		if kwargs['funcionario']:
			if pedido_servico.funcionario:
				if kwargs['funcionario'] != pedido_servico.funcionario:
					pedido_servico.funcionario_obj = funcionario_service.query_funcionario_by_id(kwargs['funcionario'])
			else:
				pedido_servico.funcionario_obj = funcionario_service.query_funcionario_by_id(kwargs['funcionario'])
		elif not kwargs['funcionario'] and kwargs['status'] == 'novo':
			pedido_servico.funcionario_obj = None
		else:
			raise ValueError('Não é permitido ficar sem responsável quando já foi iniciado ')

	if 'promob_inicial' in kwargs:
		if kwargs['promob_inicial']:
			if 'promob_inicial' in pedido_servico.servico_props:
				if kwargs['promob_inicial'] != pedido_servico.servico_props['promob_inicial']:
					pedido_servico.servico_props['promob_inicial']
			else:
				pedido_servico.servico_props['promob_inicial'] = kwargs['promob_inicial']

	if 'promob_final' in kwargs:
		if kwargs['promob_final']:
			if 'promob_final' in pedido_servico.servico_props:
				if kwargs['promob_final'] != pedido_servico.servico_props['promob_final']:
					pedido_servico.servico_props['promob_final']
			else:
				pedido_servico.servico_props['promob_final'] = kwargs['promob_final']

	if 'agendamento' in kwargs:
		if kwargs['agendamento']:
			if 'agendamento' in pedido_servico.servico_props:
				print(pedido_servico.servico_props['agendamento'])
				pedido_servico.servico_props['agendamento'].append(kwargs['agendamento'])
				print(kwargs['agendamento'])
				print(pedido_servico.servico_props['agendamento'])
			else:
				pedido_servico.servico_props['agendamento'] = [kwargs['agendamento']]

	for indx in range(3):
		key_medicao = 'medicao_%s' % indx
		if key_medicao in kwargs:
			if kwargs[key_medicao]:
				if 'agendamento' in pedido_servico.servico_props:
					if kwargs[key_medicao] != pedido_servico.servico_props['agendamento'][indx]:
						print(pedido_servico.servico_props['agendamento'])
						pedido_servico.servico_props['agendamento'][indx] = kwargs[key_medicao]
				else:
					pedido_servico.servico_props['agendamento'] = [kwargs[key_medicao]]

	# return updated_values
