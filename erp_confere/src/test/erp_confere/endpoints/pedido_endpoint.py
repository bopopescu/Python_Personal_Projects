from flask import Blueprint, render_template, url_for, request, jsonify,redirect, flash, abort
from services import servico_service
from services import ambiente_service
from services import loja_service
from services import pedido_service
from services import funcionario_service
from app_util import date_util
from services import pedido_servico_service
from flask_paginate import Pagination, get_page_args
from marshmallow import pprint
from flask_security import roles_accepted, login_required, current_user
from endpoints.exception_handler import http_error
from endpoints.forms.pedido_filter_form import PedidoFilterForm
import copy
import decimal
import jsonpickle 
import app_util.jsonpickle_handler 
import json


# Blueprint
bp = Blueprint('pedido', __name__, url_prefix='/pedido')

@bp.route('/<int:codigo_pedido>/servico/<int:codigo_servico>', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'medidor', 'projetista', 'controladora')
def pedido_servico(codigo_pedido, codigo_servico):

	is_medidor_and_medicao = current_user.roles[0].name == 'medidor' and codigo_servico == 1
	is_projetista = current_user.roles[0].name == 'projetista' and codigo_servico in [2, 3, 5, 6] 
	is_admin = current_user.roles[0].name == 'admin'
	is_controladora = current_user.roles[0].name == 'controladora'

	if is_medidor_and_medicao or is_projetista or is_admin or is_controladora:
		if request.method == 'GET':
			pedido_servico = pedido_servico_service.query_pedido_servico_by_pedido_servico(codigo_pedido, codigo_servico)
			funcionarios = funcionario_service.query_funcionarios()
			return render_template('pedido/pedido_servico.html', pedido_servico=pedido_servico, funcionarios=funcionarios)
		elif request.method == 'POST':
			
			servico_form = parse_form(request.form)

			if servico_form['acao'] == 'Atualizar':
				pedido_servico_service.atualiza(**servico_form)
				
				flash('Atualizando com sucesso', 'success')
				return redirect(url_for('pedido.pedido_servico', 
					codigo_pedido=servico_form['codigo_pedido'], codigo_servico=servico_form['codigo_servico']))
			else:
				print(request.form)
				print(servico_form)
				if servico_form['acao'] == 'Iniciar' or servico_form['acao'] == 'Agendar':
					if validate_form_agendar_iniciar(request):
						try:
							pedido_servico_service.agendar_iniciar(**servico_form)
						except Exception as e:
							flash(str(e), 'error')
						else:
							flash('Serviço iniciado com sucesso' ,'success')
					else:
						flash('Informações necessárias: funcionário e data de agendamento (no caso de Medição e Atendimento)', 'error')
				elif servico_form['acao'] == 'Concluir':

					if current_user.has_role('admin'):
						try:
							pedido_servico_service.concluir(**servico_form)
						except ValueError as err:
							flash(str(err), 'error')
						else:
							flash('Serviço concluido!')
					else:
						abort(403, 'Sem acesso')				
				elif servico_form['acao'] == 'Reabrir':
					pedido_servico_service.reabrir(**servico_form)
					flash('Serviço reaberto', 'success')
				else:
					flash('Favor informar o valor do promob para realizar a conclusão do serviço')

				return redirect(url_for('pedido.pedido_servico', 
						codigo_pedido=servico_form['codigo_pedido'], codigo_servico=servico_form['codigo_servico']))
	else:
		abort(403, 'Sem acesso')


@bp.route('/atrados', methods=['GET'])
@login_required
@roles_accepted('admin')
def pedido_servico_atrasado():
	pedidos_servicos = pedido_servico_service.query_pedidos_servicos_late()
	return render_template('admin/index.html', pedidos_servicos=pedidos_servicos)	


# @bp.route('/pedidos/<int:page>', methods=['GET', 'POST'])
@bp.route('/pedidos', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def pedidos():
	
	filter_form = PedidoFilterForm()
	filter_form.loja_filtro.choices = loja_service.query_loja_codigo_nome()
	filter_form.loja_filtro.default = None
	per_page = 5
	page = int(request.args.get('page')) if 'page' in request.args else 1

	info = {}

	if 'loja_filtro' in request.args:
		loja_filtro = request.args.get('loja_filtro')
		pedidos = pedido_service.query_pedidos_by_loja_paginated(page, per_page, loja_filtro)
		info['loja_filtro'] = loja_filtro
	elif 'status_filtro' in request.args:
		status_filtro = request.args.get('status_filtro')
		pedidos = pedido_service.query_pedidos_by_status_paginated(page, per_page, status_filtro)
		info['status_filtro'] = status_filtro
	else:
		pedidos = pedido_service.query_all_pedidos_paginated(page, per_page)

	print(info)
	return render_template('/pedido/pedidos.html', pedidos=pedidos, filter_form=filter_form, argumentos=info)

@bp.route('/<int:codigo_pedido>/pedido_servico')
@login_required
@roles_accepted('admin', 'controladora')
def pedido_servicos(codigo_pedido):
	
	pedido_servicos = pedido_servico_service.query_partial_pedido_servico_by_pedido(codigo_pedido)
	return jsonify(pedido_servicos)


@bp.route('/cadastrar', methods=["GET", "POST"])
@login_required
@roles_accepted('admin', 'controladora')
def cadastrar():
	
	if request.method == 'POST':
		pedido = build_request_form(request)
		pedido_service.create_pedido_handler(pedido)

		msg = 'Pedido cadastrado com sucesso'
		categoria = 'success'
		flash(msg, categoria)
		return redirect(url_for('pedido.cadastrar'))
	else:
		servicos = servico_service.query_all_servicos()
		ambientes = ambiente_service.query_all_ambientes()
		lojas = loja_service.query_all_lojas()

		return render_template('pedido/cadastrar.html', servicos=servicos, ambientes=ambientes, lojas=lojas)


@bp.route('/medicao', methods=['GET', 'POST'])
@login_required
@roles_accepted('medidor', 'admin')
def medicao():
	pedido_servicos = pedido_servico_service.query_pedido_servico_medicao()
	return render_template('medidor/index.html', pedido_servicos=pedido_servicos)


def ambientes_to_dict(form):
	# Ambientes
	ambientes = ambiente_service.query_all_ambientes()
	ambientes_sent = {'ambientes': []}
	for ambiente in ambientes:
		nome_ambiente = ambiente.nome.replace(' ', '-').lower()
		amb = {}
		if nome_ambiente in form:
			amb['nome'] = ambiente.nome
			amb['quantidade'] = form['quantidade-' + nome_ambiente]
			ambientes_sent['ambientes'].append(amb)

	return ambientes_sent


@bp.route('/projetista', methods=['GET'])
@login_required
@roles_accepted('projetista', 'admin')
def projetista():
	per_page = 10
	if 'page' in request.args:
		page = int(request.args['page'])
	else:
		page = 1

	pedido_servicos = pedido_servico_service.query_all_pedido_servicos_projetista(page, per_page)
	return render_template('projetista/index.html', pedido_servicos=pedido_servicos)


@bp.route('/aprovar', methods=['GET'])
@login_required
@roles_accepted('admin')
def aprovar():
	pedido_servicos = pedido_servico_service.query_pedido_servico_concluido()
	return render_template('pedido/aprovar.html', pedido_servicos=pedido_servicos)


@bp.route('/liberado/<int:codigo_pedido>/<int:codigo_servico>', methods=['GET'])
@login_required
@roles_accepted('admin')
def liberado(codigo_pedido, codigo_servico):

	pedido_servico = pedido_servico_service.aprovar(codigo_pedido=codigo_pedido, codigo_servico=codigo_servico)
	return redirect(url_for('pedido.aprovar'))


def validate_form_agendar_iniciar(request):

	'''
		function validates if the required informations are present in the request
		In this case: funcionario and data-medicao|medicao-0|medicao-1|medicao-2 
	'''
	if request.form['funcionario'] == '' and request.form['status'] in ['iniciado', 'agendado', 'novo']:
		return True

	if request.form['nome-servico'] == 'medicao' or request.form['nome-servico'] == 'atendimento':
		if 'agendamento' in request.form:
			if request.form['agendamento'] == '':
				return False
		else:
			for indx in range(3):
				chave = 'medicao-%s' % indx
				if chave in request.form:
					if request.form[chave] != '':
						return True
			return False

	return True

def parse_form(form):

	parsed_form = {}
	for key in form:
		if form[key] == '':
			parsed_form[key.replace('-', '_')] = None
		else:
			if key == 'promob-inicial' or key == 'promob-final':
				parsed_form[key.replace('-', '_')] = float(form[key].replace(',', '.'))
			elif key == 'agendamento':
				parsed_form[key] = copy.copy(form.getlist('agendamento'))
			else:
				parsed_form[key.replace('-', '_')] = form[key]

	return parsed_form

def build_request_form(request):
	# Pedido
	pedido = {}
	pedido['numero_pedido'] = request.form['numero-pedido']
	pedido['valor_pedido'] = float(request.form['valor-pedido'].replace(',', '.'))
	pedido['data_entrada'] = date_util.convert_form_date_to_date(request.form['data-entrada'])
	pedido['loja'] = request.form['loja']
	# Cliente
	pedido['nome'] = request.form['nome-cliente']
	pedido['sobrenome'] = request.form['sobrenome-cliente']
	pedido['email'] = request.form['email']
	pedido['tel_residencial'] = request.form['telefone-residencial']
	pedido['tel_celular'] = request.form['telefone-celular']
	# Endereço
	pedido['cep'] = request.form['cep']
	pedido['endereco'] = request.form['endereco']
	pedido['complemento'] = request.form['complemento']
	pedido['bairro'] = request.form['bairro']
	pedido['numero'] = request.form['numero']
	# Serviços
	pedido['servicos'] = request.form.getlist('servicos')
	pedido['ambientes'] = ambientes_to_dict(request.form)

	return pedido