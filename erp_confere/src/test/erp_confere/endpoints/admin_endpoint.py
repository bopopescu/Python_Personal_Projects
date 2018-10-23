from flask import Blueprint, url_for, render_template, redirect, flash, request
from flask_security import login_required, roles_accepted, current_user
from datetime import date, datetime
from endpoints.forms import UsuarioRegistration, DashFilterForm
from services import funcao_service, admin_service, pedido_servico_service
from model import User, Funcionario
from app_util import create_system_user
from endpoints.charts import pedido_loja_bar_char, funcionario_pedido_mes_pie_chart, render_graphics

import calendar

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/', methods=['GET'])
@login_required
@roles_accepted('admin')
def index():

	form = DashFilterForm()
	print(form.is_submitted())
	if all(key in request.args for key in ['data_inicio', 'data_fim']):

		# Transform the string into date 
		data_fim = datetime.strptime(request.args.get('data_fim'), '%d/%m/%Y').date()
		data_inicio = datetime.strptime(request.args.get('data_inicio'), '%d/%m/%Y').date()

		if data_inicio > data_fim:
			flash('Data início maior que data fim', 'error')
			return render_template('admin/index.html', the_script=None, the_div=[], the_form=form)

	else:
		curdate = date.today()
		last_day_of_month = calendar.monthrange(curdate.year, curdate.month)[1]
		data_fim = date(curdate.year, curdate.month, last_day_of_month)
		data_inicio = date(curdate.year, curdate.month, 1)
		
	
	lojas_quantidade = pedido_servico_service.query_count_pedidos_servicos_by_loja(data_inicio, data_fim)
	funcionarios = pedido_servico_service.query_count_pedido_servico_by_funcionario(data_inicio, data_fim)

	retorno = []

	
	is_ok_render = False

	if len(lojas_quantidade) > 0:
		dados_loja = {'data_fim': data_fim, 'data_inicio': data_inicio, 'lojas': [], 'quantidade': []}
		for row in lojas_quantidade:
			dados_loja['lojas'].append(row[0])
			dados_loja['quantidade'].append(row[1])

		graphic2 = pedido_loja_bar_char(dados_loja)
		retorno.append(graphic2)
		is_ok_render = True

	print(len(funcionarios))
	if len(funcionarios) > 0:
		dados_funcionario = {'data_fim': data_fim, 'data_inicio': data_inicio}
		for row in funcionarios:
			nome_completo = row[1].split(' ')
			nome = nome_completo[0]
			sobrenome = nome_completo[-1]

			fullname = nome + ' ' + sobrenome
			dados_funcionario[fullname] = row[2]

		graphic1 = funcionario_pedido_mes_pie_chart(dados_funcionario)
		retorno.append(graphic1)
		is_ok_render = True

	if is_ok_render:
		script, div = render_graphics(retorno)
		return render_template('admin/index.html', the_script=script, the_div=div, the_form=form)
	
	flash('Não há graficos no periodo de {} à {}'.format(data_inicio.strftime('%d/%m/%Y'), data_fim.strftime('%d/%m/%Y')), 'error')
	return render_template('admin/index.html', the_script=None, the_div=[], the_form=form)

@bp.route('/registrar/<int:user_id>', methods=['GET'])
@bp.route('/registrar', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def registrar_usuario(**kwargs):

	try:
		if 'user_id' in kwargs:
			user = admin_service.query_usuario_by_id(kwargs['user_id'])
			form = UsuarioRegistration(nome=user.funcionario.nome, sobrenome=user.funcionario.sobrenome, 
				email=user.email, numero_residencial=user.funcionario.telefone_residencial, 
				numero_celular=user.funcionario.telefone_celular, ativo=user.active)
		else:	
			form = UsuarioRegistration()
		
		form.funcao.choices = [(funcao.id, funcao.name.capitalize()) for funcao in funcao_service.query_funcoes()]
		if request.method == 'GET':
			return render_template('admin/cadastrar_usuario.html', form=form)
		elif request.method == 'POST':
			if form.validate_on_submit():
				obj_dict = handle_form_user_registration(form)
				admin_service.new_user_handler(obj_dict['usuario'], obj_dict['funcionario'], form.data['funcao'])
				flash('Usuario criado com sucesso. Senha: %s' % obj_dict['usuario'].password, 
						'success')
				return redirect(url_for('admin.registrar_usuario'))
			else:
				return render_template('admin/cadastrar_usuario.html', form=form)
	except Exception as e:
		pass # Erro 500


@bp.route('/usuarios', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def usuarios():
	usuarios = admin_service.query_usuarios()
	return render_template('admin/usuarios.html', usuarios=usuarios)


def handle_form_user_registration(form):
	funcionario = Funcionario(nome=form.data['nome'], sobrenome=form.data['sobrenome'], 
		telefone_residencial=form.data['numero_residencial'], telefone_celular=form.data['numero_celular'], 
		cargo=form.data['cargo'], data_admissao=date.today())
	username = create_system_user(funcionario.nome, funcionario.sobrenome)
	usuario = User(email=form.data['email'], username=username, active=form.data['ativo'])

	return {'funcionario': funcionario, 'usuario': usuario}
