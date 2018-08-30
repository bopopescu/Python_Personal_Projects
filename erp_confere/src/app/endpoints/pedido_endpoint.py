from flask import Blueprint, render_template, url_for, request, jsonify,redirect, flash
from services import servico_service
from services import ambiente_service
from services import loja_service
from services import pedido_service
from services import funcionario_service
from app_util import date_util
from services import pedido_servico_service
from flask_paginate import Pagination, get_page_args
import jsonpickle 
import app_util.jsonpickle_handler 
import json


# Blueprint
bp = Blueprint('pedido', __name__, url_prefix='/pedido')

@bp.route('/<int:codigo_pedido>/servico/<int:codigo_servico>', methods=['GET', 'POST'])
def pedido_servico(codigo_pedido, codigo_servico):

	if request.method == 'GET':
		pedido_servico = pedido_servico_service.get_pedido_servico_by_pedido_servico(codigo_pedido, codigo_servico)
		funcionarios = funcionario_service.query_funcionarios()
		return render_template('pedido/pedido_servico.html', pedido_servico=pedido_servico, funcionarios=funcionarios)
	elif request.method == 'POST':
		
		# Construct a new and clean object to send to pedido_servico_service
		servico_form = {}
		if 'data-medicao-agendada' in request.form:
			servico_form['agendamento'] = None if request.form['data-medicao-agendada'] == '' else request.form['data-medicao-agendada']
		if 'funcionario' in request.form:
			servico_form['funcionario'] = None if request.form['funcionario'] == '' else request.form['funcionario']
		if 'comentario' in request.form:
			servico_form['comentario'] = None if request.form['comentario'] == '' else request.form['comentario']
		if 'codigo-pedido' in request.form:
			servico_form['codigo_pedido'] = request.form['codigo-pedido']
		if 'codigo-servico' in request.form:
			servico_form['codigo_servico'] = request.form['codigo-servico']
		if 'promob-inicial' in request.form:
			servico_form['promob_inicial'] = None if request.form['promob-inicial'] == '' else request.form['promob-inicial']
		if 'promob_final' in request.form:
			servico_form['promob_final'] = None if request.form['promob-final'] == '' else request.form['promob-final']
		if 'status' in request.form:
			servico_form['status'] = request.form['status']

		print(servico_form)
		print(request.form)
		# Decide which service type is and its status 
		if request.form['acao'] == 'Atualizar':
			pedido_servico_service.update_pedido_servico(**servico_form)

			flash('Atualizando com sucesso', 'success')
			return redirect(url_for('pedido.pedido_servico', 
				codigo_pedido=servico_form['codigo_pedido'], codigo_servico=servico_form['codigo_servico']))
		else:
			if request.form['acao'] == 'Iniciar' or request.form['acao'] == 'Agendar':
				# Update data_inicio with the current date and can't have funcionario None
				# If is servico == medicao or servico == atendimento then data_agendamento is
				# required
				if validate_form_agendar_iniciar(request):
					# update
					print('foi aqui')
					pass
				else:
					flash('Informações necessárias: Funcionário e data de agendamento (Medição e Liberação)', 'error')
					return redirect(url_for('pedido.pedido_servico', 
						codigo_pedido=request.form['codigo-pedido'], codigo_servico=request.form['codigo-servico']))
 

@bp.route('/')
def pedido():
	return render_template('pedido.html')

@bp.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
	search = False

	page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='page_parameter')

	# print('Page: {} | Per page: {} | Offset: {}'.format(page, per_page, offset))

	q = request.args.get('q')
	if q:
		search = True
	
	pedidos = pedido_service.query_pedidos()

	print('List size: {}'.format(len(pedidos)))

	pagination = Pagination(page=page, total=len(pedidos), per_page=per_page, search=search, record_name='pedidos',
		css_framework='bootstrap4') 

	return render_template('pedido/pedidos.html', pedidos=pedidos, pagination=pagination)

@bp.route('/<int:codigo_pedido>/pedido_servico')
def pedido_servicos(codigo_pedido):
	
	pedido_servicos = pedido_servico_service.get_pedido_servico_by_servico(codigo_pedido)
	jason = [jsonpickle.encode(pedido_servico, unpicklable=False) for pedido_servico in pedido_servicos]
	print(type(pedido_servicos[0].data_inicio))

	return jsonify(jason)

@bp.route('/cadastrar', methods=["GET", "POST"])
def cadastrar():
	
	if request.method == 'POST':
		
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

		pedido_service.create_pedido_handler(pedido)

		return redirect(url_for('pedido.cadastrar'))
	else:
		servicos = servico_service.get_all_servicos()
		ambientes = ambiente_service.get_all_ambientes()
		lojas = loja_service.query_all_lojas()

		return render_template('pedido/cadastrar.html', servicos=servicos, ambientes=ambientes, lojas=lojas)



def ambientes_to_dict(form):
	# Ambientes
	ambientes = ambiente_service.get_all_ambientes()
	ambientes_sent = []
	for ambiente in ambientes:
		nome_ambiente = ambiente.nome.replace(' ', '-').lower()
		amb = {}
		if nome_ambiente in form:
			amb['nome'] = ambiente.nome
			amb['quantidade'] = form['quantidade-' + nome_ambiente]
			ambientes_sent.append(amb)

	return ambientes_sent


def validate_form_agendar_iniciar(request):

	if request.form['funcionario'] == '':
		return False

	if request.form['nome-servico'] == 'medicao' or request.form['nome-servico'] == 'atendimento':
		if 'data-medicao-agendada' in request.form:
			if request.form['data-medicao-agendada'] == '':
				return False
		else:
			return False

	return True

