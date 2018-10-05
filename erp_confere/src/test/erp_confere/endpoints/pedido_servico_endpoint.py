from flask import Blueprint, Flask, render_template, flash, request, redirect, url_for
from flask_security import login_required, roles_accepted
from model.models import PedidoServico
from services import pedido_service, loja_service, pedido_servico_service
from endpoints.forms.pedido_servico_filtro_form import PedidoServicoListaFiltroForm

bp = Blueprint('pedido_servico', __name__, url_prefix='/pedido_servico')

@bp.route('/lista', methods=['GET'])
@login_required
@roles_accepted('admin')
def lista():

	per_page = 10
	if 'page' in request.args:
		page = int(request.args['page'])
	else:
		page = 1

	filter_form = PedidoServicoListaFiltroForm()
	filter_form.loja.choices = loja_service.query_loja_codigo_nome()
	filter_form.loja.default = None

	if 'filtrar_por' in request.args:
		filtro_utilizado = request.args['filtrar_por']
	else:
		filtro_utilizado = ''

	arguments = {}

	if filtro_utilizado == 'loja':
		pedidos_servicos = pedido_servico_service.query_pedido_servico_loja(page, per_page, request.args['loja'])
		arguments['loja'] = request.args['loja']
	elif filtro_utilizado == 'status':
		if filtro_utilizado == 'atrasdo':
			pedidos_servicos = pedido_servico_service.query_pedidos_servicos_late(page, per_page)
		else:
			pedidos_servicos = pedido_servico_service.query_pedido_servico_status(page, per_page, request.args['status'])

		arguments['status'] = request.args['status']
	elif filtro_utilizado == 'pedido_codigo':
		pedidos_servicos = pedido_servico_service.query_pedido_servico_pedido(page, per_page, request.args['pedido_codigo'])
		arguments['pedido_codigo'] = request.args['pedido_codigo']

	else:
		pedidos_servicos = pedido_servico_service.query_all_pedido_servicos(page, per_page)	
	

	return render_template('pedido_servico/lista.html', pedidos_servicos=pedidos_servicos, form=filter_form, arguments=arguments)



