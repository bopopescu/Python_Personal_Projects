from flask import Blueprint, url_for, render_template, redirect, flash, request
from flask_security import login_required, roles_accepted, current_user
from datetime import date
from endpoints.forms.usuario import UsuarioRegistration
from services import funcao_service, admin_service
from model.models import User, Funcionario
from app_util import create_system_user

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/', methods=['GET'])
@login_required
@roles_accepted('admin')
def index():
	return redirect(url_for('pedido.pedido_servico_atrasado'))

@bp.route('/registrar/<int:user_id>', methods=['GET'])
@bp.route('/registrar', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def registrar_usuario(**kwargs):
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
