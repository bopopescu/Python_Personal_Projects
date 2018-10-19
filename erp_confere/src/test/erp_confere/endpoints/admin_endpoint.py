from flask import Blueprint, url_for, render_template, redirect, flash, request
from flask_security import login_required, roles_accepted, current_user
from datetime import date
from endpoints.forms import UsuarioRegistration
from services import funcao_service, admin_service, pedido_servico_service
from model import User, Funcionario
from app_util import create_system_user
from endpoints.charts import pedido_loja_bar_char, funcionario_pedido_mes_pie_chart

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/', methods=['GET'])
@login_required
@roles_accepted('admin')
def index():

	data_fim = date(2019, 9, 1)
	data_inicio = date(2018, 9, 1)
	# loja_quantidade = pedido_servico_service.query_count_pedidos_servicos_by_loja(data_inicio, data_fim)

	result_set = pedido_servico_service.query_count_pedido_servico_by_funcionario(data_inicio, data_fim)

	data = {'data_fim': data_fim, 'data_inicio': data_inicio}

	for row in result_set:
		nome_completo = row[1].split(' ')
		nome = nome_completo[0]
		sobrenome = nome_completo[-1]

		fullname = nome + ' ' + sobrenome
		data[fullname] = row[2]

	# data = {'lojas': [], 'quantidade': [], 'data_inicio': data_inicio, 'data_fim': data_fim}

	# for column in loja_quantidade:
	# 	data['lojas'].append(column[0])
	# 	data['quantidade'].append(column[1])

	script, div = funcionario_pedido_mes_pie_chart(data)

	print(script)
	
	return render_template('admin/index.html', the_script=script, the_div=div)

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
