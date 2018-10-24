import app_util.constants as const
import json
import app_util.json_util as json_util
import services.servico_service as servico_service
import copy
import datetime
import contextlib
from model import PedidoServico, Servico, TipoValor, StatusPedido, Loja, Pedido, Funcionario, ServicoEnum, StatusPedidoServico
from services import funcionario_service
from services import pedido_service
from services import feriado_service
from persistence import db
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func, text

def json_to_model(pedido, servico):
	status = json_util.dict_to_str({'status': 'novo'})
	return PedidoServicoModel(pedido, servico, None, 0, None, None, status)	


def generate_pedido_servico(pedido, servico):
	status = {'status': 'novo'}
	return PedidoServico(pedido_obj=pedido, servico_obj=servico, funcionario_obj=None, 
		valor_comissao=0, data_inicio=None, data_fim=None, servico_props=status)


def report_pedido_servico_funcionario_periodo(page, per_page, codigo_funcionario, data_inicio, data_fim):
	return db.session.query(PedidoServico)\
					.join(Pedido)
					.join(Funcionario)\
					.filter(Funcionario.codigo == codigo_funcionario, Pedido.data_entrada.between(data_inicio, data_fim))


def report_pedido_servico_comissao_funcionario_period(page, per_page, codigo_funcionario, data_inicio, data_fim):
	return db.session.query(Funcionario.codigo, 
							func.concat(Funcionario.nome + ' ' + Funcionario.sobrenome).label('Funcionario'),
							func.sum(PedidoServico.valor_comissao))\
					.join(PedidoServico)\
					.join(Pedido)\
					.filter(Pedido.data_entrada.between(data_inicio, data_fim), 
							Funcionario.codigo == codigo_funcionario,
							PedidoServico.servico_props['status'] == StatusPedidoServico.LIBERADO.value)\
					.group_by(Funcionario.codigo, 
							func.concat(Funcionario.nome + ' ' + Funcionario.sobrenome).label('Funcionario'))\
					.paginate(page=page, per_page=per_page, error_out=False)

def query_first_pedido_servico_by_pedido(codigo_pedido):
	return db.session.query(PedidoServico, Servico)\
					.join(PedidoServico.servico_obj)\
					.with_entities(func.min(PedidoServico.servico))\
					.filter(PedidoServico.pedido == codigo_pedido)\
					.order_by(Servico.sequencia.asc())\
					.one()


def query_last_pedido_servico_by_pedido(codigo_pedido):
	return db.session.query(PedidoServico, Servico)\
					.join(PedidoServico.servico_obj)\
					.with_entities(func.max(PedidoServico.servico))\
					.filter(PedidoServico.pedido == codigo_pedido)\
					.order_by(Servico.sequencia.asc())\
					.one()

def query_count_pedidos_servicos_by_loja(data_inicio, data_fim):

	return db.session.query(Loja.nome, func.count(1).label('quantidade')) \
					.join(Pedido) \
					.filter(Pedido.data_entrada.between(data_inicio, data_fim)) \
					.group_by(Loja.nome) \
					.all()
					
def query_count_pedido_servico_by_funcionario(data_inicio, data_fim):

	return db.session.query(Funcionario.codigo, 
							Funcionario.nome + ' ' + Funcionario.sobrenome, 
							func.count(1).label('quantidade'))\
				.join(PedidoServico) \
				.join(Pedido) \
				.filter(Pedido.data_entrada.between(data_inicio, data_fim)) \
				.group_by(Funcionario.codigo) \
				.all()


def query_pedido_servico_medicao_by_funcionar(page, per_page, codigo_funcionario):
	return db.session.query(PedidoServico)\
					.filter(((PedidoServico.funcionario == codigo_funcionario) | (PedidoServico.funcionario == None)),
						PedidoServico.servico == 1,
						((PedidoServico.servico_props['status'] == 'agendado') | (PedidoServico.servico_props['status'] == 'novo')))\
					.paginate(page=page, per_page=per_page, error_out=False)


def query_pedidos_servicos_late(page, per_page):
	return db.session.query(PedidoServico)\
		.filter(PedidoServico.data_fim_previsao > datetime.date.today(), PedidoServico.data_fim is None)\
		.paginate(page=page, per_page=per_page, error_out=False)


def query_pedido_servico_by_pedido(codigo_pedido):
	return PedidoServico.query.filter_by(pedido=codigo_pedido).all()


def query_pedido_servico_available_to_start(page, per_page):

	subqueri = db.session.query(PedidoServico.pedido.label('pedido'), func.min(PedidoServico.servico).label('servico'))\
					.join(Servico)\
 					.filter(PedidoServico.data_fim == None, PedidoServico.servico_props['status'] == 'novo',
 						Servico.codigo.notin_((ServicoEnum.MEDICAO.value, ServicoEnum.ATENDIMENTO.value)))\
 					.group_by(PedidoServico.pedido).subquery()

	return db.session.query(PedidoServico)\
			.filter(PedidoServico.pedido == subqueri.c.pedido, PedidoServico.servico == subqueri.c.servico)\
			.paginate(page=page,per_page=per_page,error_out=False)


def query_pedido_servico_by_servico(codigo_pedido):
	pedido_servicos = query_pedido_servico_by_pedido(codigo_pedido)
	return pedido_servicos


def query_pedido_servico_by_pedido_servico(codigo_pedido, codigo_servico):
	return PedidoServico.query.filter_by(pedido=codigo_pedido, servico=codigo_servico).one()


def query_all_pedido_servicos_projetista(page, per_page):
	return db.session.query(PedidoServico)\
		.filter(PedidoServico.servico.in_([2, 3, 5, 6]), PedidoServico.servico_props['status'] == 'novo')\
		.paginate(page=page, per_page=per_page, error_out=False)


def query_all_pedido_servicos(page, per_page):
	return db.session.query(PedidoServico)\
		.paginate(page=page, per_page=per_page, error_out=False)


def query_pedido_servico_medicao(page, per_page):
	return db.session.query(PedidoServico).filter(PedidoServico.servico == 1, 
		((PedidoServico.servico_props['status'] == 'agendado') | (PedidoServico.servico_props['status'] == 'novo')))\
		.paginate(page=page, per_page=per_page, error_out=False)


def query_pedido_servico_status(page, per_page, status):
	return db.session.query(PedidoServico)\
			.filter(PedidoServico.servico_props['status'] == status)\
			.paginate(page=page, per_page=per_page, error_out=False)


def query_pedido_servico_loja(page, per_page, loja):
	return db.session.query(PedidoServico)\
			.join(PedidoServico.pedido_obj)\
			.join(Loja)\
			.filter(Loja.codigo == loja)\
			.paginate(page=page, per_page=per_page, error_out=False)


def query_pedido_servico_pedido(page, per_page, numero):
	return db.session.query(PedidoServico)\
			.join(PedidoServico.pedido_obj)\
			.filter(Pedido.numero == numero)\
			.paginate(page=page, per_page=per_page, error_out=False)


def query_partial_pedido_servico_by_pedido(codigo_pedido):
	result_set = (db.session.query(PedidoServico, Servico)\
		.join(PedidoServico.servico_obj) \
		.join(PedidoServico.funcionario_obj, isouter=True)\
		.with_entities(PedidoServico.pedido, PedidoServico.servico, Servico.nome_real, PedidoServico.servico_props, 
			Funcionario.nome + ' ' + Funcionario.sobrenome, PedidoServico.data_fim_previsao, PedidoServico.data_inicio_previsao) \
		.filter(PedidoServico.pedido == codigo_pedido).all())

	retorno = []
	for row in result_set:
		linha = {}
		linha['pedido'] = row[0]
		linha['servico'] = row[1]
		linha['nome'] = row[2]
		linha['status'] = row[3]['status'].capitalize()
		linha['nome_funcionario'] = row[4]
		linha['data_inicio_previsao'] = row[5].strftime('%d/%m/%Y')
		linha['data_fim_previsao'] = row[6].strftime('%d/%m/%Y')
		retorno.append(linha) 

	db.session.close()
	return retorno


def query_pedido_servico_concluido():
	return db.session.query(PedidoServico).filter(PedidoServico.servico_props['status'] == 'concluido').all()


def agendar_iniciar(**kwargs):	
	pedido_servico_original = query_pedido_servico_by_pedido_servico(kwargs['codigo_pedido'], kwargs['codigo_servico'])
	is_changeable = is_pedido_servico_status_changeable(pedido_servico_original)

	if is_changeable:

		if pedido_servico_original.servico_props['status'] == 'novo':

			codigo_primerio_servico = query_first_pedido_servico_by_pedido(pedido_servico_original.pedido)[0]

			if codigo_primerio_servico == pedido_servico_original.servico:
				pedido_servico_original.pedido_obj.status = StatusPedido.iniciado
				pedido_servico_original.pedido_obj.data_inicio = datetime.date.today()

			if kwargs['funcionario']:
				pedido_servico_original.funcionario = kwargs['funcionario']
			elif not kwargs['funcionario'] and pedido_servico_original.funcionario_obj:
				pedido_servico_original.funcionario_obj = None
			
			if kwargs['comentario']:
				pedido_servico_original.servico_props['comentario'] = kwargs['comentario']
			
			pedido_servico_original.data_inicio = datetime.date.today()

			
			if pedido_servico_original.servico_obj.nome in ['medicao', 'atendimento']:
				agendar(pedido_servico_original, **kwargs)
			else:
				iniciar(pedido_servico_original, **kwargs)

			db.session.commit()


def iniciar(pedido_servico, **kwargs):
	if pedido_servico.servico_obj.nome == 'subir_paredes':
		if kwargs['promob_inicial']:
			pedido_servico.servico_props['promob_inicial'] = kwargs['promob_inicial']
	elif pedido_servico.servico_obj.nome == 'liberacao':
		if kwargs['promob_final']:
			pedido_servico.servico_props['promob_final'] = kwargs['promob_final']

	pedido_servico.servico_props['status'] = 'iniciado'


def agendar(pedido_servico, **kwargs):
	if 'agendamento' in kwargs:
		pedido_servico.servico_props['agendamento'] = kwargs['agendamento']
	elif 'agendamento' not in kwargs and 'agendamento' not in pedido_servico.servico_props: 
		raise ValueError('Favor informar uma data de agendamento')

	pedido_servico.servico_props['status'] = 'agendado'


def atualiza(**kwargs):	
	pedido_servico = query_pedido_servico_by_pedido_servico(kwargs['codigo_pedido'], kwargs['codigo_servico'])
	if pedido_servico.servico_props['status'] in ['novo', 'agendado', 'iniciado']:
		
		pedido_servico.funcionario_obj = funcionario_service.query_funcionario_by_id(kwargs['funcionario'])
		
		if 'comentario' in pedido_servico.servico_props:
			if kwargs['comentario']:
				pedido_servico.servico_props['comentario'] = kwargs['comentario']
			else:
				pedido_servico.servico_props.pop('comentario', None)
		else:
			if kwargs['comentario'] is not None:
				pedido_servico.servico_props['comentario'] = kwargs['comentario']

		if pedido_servico.servico_obj.nome in ['medicao', 'atendimento']:
			pedido_servico.servico_props['agendamento'] = kwargs['agendamento']

		if pedido_servico.servico_obj.nome in ['subir_paredes', 'liberacao']:
			promob = 'promob_inicial' if pedido_servico.servico_obj.nome == 'subir_paredes' else 'promob_final'
			if promob in pedido_servico.servico_props:
				if kwargs[promob]:
					pedido_servico.servico_props[promob] = kwargs[promob]
				else:
					pedido_servico.servico_props.pop(promob, None)
			else:
				if kwargs[promob] is not None:
					pedido_servico.servico_props[promob] = kwargs[promob]

		db.session.commit()
	else:
		raise ValueError('Os dados só podem ser atualizados se o serviço não estiver concluído ou liberado')


def concluir(**kwargs):

	pedido_servico = query_pedido_servico_by_pedido_servico(kwargs['codigo_pedido'], kwargs['codigo_servico'])
	pedido_serivco_changeable = is_pedido_servico_status_changeable(pedido_servico)

	if pedido_serivco_changeable:
		if pedido_servico.servico_props['status'] in ['agendado', 'iniciado']:

			codigo_servico = query_last_pedido_servico_by_pedido(pedido_servico.pedido)[0]

			if codigo_servico == pedido_servico.servico:
				pedido_servico.pedido_obj.status = StatusPedido.concluido
				pedido_servico.pedido_obj.data_fim = datetime.date.today()

			if kwargs['funcionario']:
				if  kwargs['funcionario'] != pedido_servico.funcionario:
					pedido_servico.funcionario_obj = funcionario_service.query_funcionario_by_id(kwargs['funcionario'])
			else:
				raise ValueError('Favor informar o funcionário')

			if kwargs['comentario']:
				if kwargs['comentario'] != pedido_servico.servico_props['comentario']:
					pedido_servico.servico_props['comentario'] = kwargs['comentario']

			if pedido_servico.servico_obj.nome in ['subir_paredes', 'liberacao']:
				promob = 'promob_inicial' if pedido_servico.servico_obj.nome == 'subir_paredes' else 'promob_final'

				if promob in kwargs:
					if kwargs[promob]:
						pedido_servico.servico_props[promob] = kwargs[promob]
					else:
						if promob in pedido_servico.servico_props:
							raise ValueError('Não é possível deixar o valor do promob em branco')
				if promob not in pedido_servico.servico_props:
						raise ValueError('Não é possível concluir sem o promob')

			pedido_servico.servico_props['status'] = 'concluido'
			pedido_servico.data_fim = datetime.date.today()

			if pedido_servico.servico_obj.tipo_valor == TipoValor.especie.value:
				pedido_servico.valor_comissao = pedido_servico.servico_obj.valor
			elif pedido_servico.servico_obj.tipo_valor == TipoValor.porcentagem.value:
				pedido_servico.valor_comissao = pedido_servico.servico_obj.valor * pedido_servico.pedido_obj.valor
			if is_pedido_finalizado(pedido_servico):
				pedido_servico.pedido_obj.data_fim = datetime.date.today()

			db.session.commit()


def aprovar(**kwargs):
	pedido_servico = query_pedido_servico_by_pedido_servico(kwargs['codigo_pedido'], kwargs['codigo_servico'])

	if pedido_servico:
		if pedido_servico.servico_props['status'] == 'concluido':
			pedido_servico.servico_props['status'] = 'liberado'
			
			db.session.commit()
		else:
			raise ValueError('Servico não está marcado como concluído')
	else:
		raise NoResultFound('Não foi possível encontrar o pedido solicitado')


def reabrir(**kwargs):
	nome_servico = kwargs['nome_servico']
	current_status = kwargs['status']
	pedido_servico = query_pedido_servico_by_pedido_servico(kwargs['codigo_pedido'], kwargs['codigo_servico'])

	if current_status == 'concluido':
		if nome_servico == 'medicao' or nome_servico == 'atendimento':
			pedido_servico.servico_props['status'] = 'agendado'
		else:
			pedido_servico.servico_props['status'] = 'iniciado'
		
		db.session.commit()


# def validate_promob(**kwargs):
# 	return 'promob_inicial' in kwargs or 'promob_final' in kwargs


def calculate_end_date_pedido_servico(data_corrente, dias_servico):
	feriados = feriado_service.query_feriados_to_come(data_corrente)

	data_final = data_corrente + datetime.timedelta(days=1)

	dias_restantes_para_verificar = 0
	while dias_restantes_para_verificar < dias_servico:
		
		if data_final not in feriados or data_final.weekday() != 6: # 6 stands for Sunday
			dias_restantes_para_verificar += 1 

		data_final = data_final + datetime.timedelta(days=1)

	return data_final

def calculate_start_date_pedido_servico(data_corrente):
	feriados = feriado_service.query_feriados_to_come(data_corrente, 5)

	data_inicio = copy.copy(data_corrente)
	dias_restantes_para_verificar = 0
	while dias_restantes_para_verificar < 1:
		if data_inicio not in feriados or data_inicio.weekday() != 6: # 6 stands for Sunday
			dias_restantes_para_verificar += 1 

		data_inicio = data_inicio + datetime.timedelta(days=1)

	return data_inicio



def validate_agendamento(**kwargs):
	if len(kwargs['agendamento']) > 0:
		return True
	return False


def is_pedido_servico_status_changeable(pedido_servico):
	previous_state = None
	
	try:
		previous_state = db.session.query(PedidoServico, Servico)\
			.join(PedidoServico.servico_obj)\
			.with_entities(PedidoServico.servico_props['status'])\
			.filter(PedidoServico.pedido == pedido_servico.pedido, PedidoServico.servico < pedido_servico.servico)\
			.order_by(Servico.sequencia.desc())\
			.limit(1)\
			.one()[0]
	except NoResultFound as e:
		previous_state = None
	
	is_changeable = previous_state == 'concluido' or previous_state == 'liberado' or not previous_state
	if is_changeable:
		return True
	
	raise ValueError('Favor encerrar devidamente o serviço anterior')


def is_pedido_finalizado(pedido_servico):
	'''
		If there aren't any pedido_servico left to execute, then the pedido is finished
	'''
	try:
		db.session.query(PedidoServico, Servico)\
			.join(PedidoServico.servico_obj)\
			.with_entities(PedidoServico.servico_props['status'])\
			.filter(PedidoServico.pedido == pedido_servico.pedido, PedidoServico.servico > pedido_servico.servico)\
			.order_by(Servico.sequencia.desc())\
			.limit(1)\
			.one()[0]
	except NoResultFound as e:
		return True
	else:
		return False


def validate_from_form(pedido_servico, **kwargs):

	# updated_values = copy.deepcopy(pedido_servico)
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
		elif not kwargs['funcionario'] and kwargs['status'] in ['novo', 'iniciado', 'agendado']:
			pedido_servico.funcionario_obj = None
		else:
			raise ValueError('Não é permitido ficar sem responsável quando já foi iniciado ')

	if 'promob_inicial' in kwargs:
		if kwargs['promob_inicial']:
			if 'promob_inicial' in pedido_servico.servico_props:
				if kwargs['promob_inicial'] != pedido_servico.servico_props['promob_inicial']:
					pedido_servico.servico_props['promob_inicial'] = kwargs['promob_inicial']
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
				pedido_servico.servico_props['agendamento'] = kwargs['agendamento']
			else:
				pedido_servico.servico_props['agendamento'] = kwargs['agendamento']		

	if 'agendamento' in kwargs:
		if kwargs['agendamento']:
			if 'agendamento' in pedido_servico.servico_props:	
				pedido_servico.servico_props['agendamento'] = kwargs['agendamento']
			else:
				pedido_servico.servico_props['agendamento'] = kwargs['agendamento']

	# agendamentos = len(pedido_servico.servico_props['agendamento'])
	# for indx in range(agendamentos):
	# 	key_medicao = 'medicao_%s' % indx
	# 	if key_medicao in kwargs:
	# 		if kwargs[key_medicao]:
	# 			if 'agendamento' in pedido_servico.servico_props:
	# 				if kwargs[key_medicao] != pedido_servico.servico_props['agendamento'][indx]:
	# 					print(pedido_servico.servico_props['agendamento'])
	# 					pedido_servico.servico_props['agendamento'].append(kwargs[key_medicao])
	# 			else:
	# 				pedido_servico.servico_props['agendamento'] = [kwargs[key_medicao]]

	# return updated_values


