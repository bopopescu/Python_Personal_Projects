from flask import Blueprint, render_template, url_for, request, jsonify,redirect
from services import servico_service
from services import ambiente_service
from services import loja_service
from services import pedido_service
from app_util import date_util
from services import pedido_servico_service
import jsonpickle 
import json


# Blueprint
bp = Blueprint('pedido', __name__, url_prefix='/pedido')

@bp.route('/')
def pedido():
	return render_template('pedido.html')

@bp.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
	'''
		Carregar os pedidos com os objetos necessários
	'''
	pedidos = pedido_service.query_pedidos()
	return render_template('pedido/pedidos.html', pedidos=pedidos)

@bp.route('/<int:codigo_pedido>/pedido_servico')
def pedido_servicos(codigo_pedido):
	
	pedido_servicos = pedido_servico_service.get_pedido_servico_by_servico(codigo_pedido)
	jason = [jsonpickle.encode(pedido_servico, unpicklable=False) for pedido_servico in pedido_servicos]
	print(jason)

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