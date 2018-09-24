from flask import Blueprint, url_for, render_template, redirect, flash, request
from flask_security import login_required, roles_accepted, current_user
from datetime import date
from endpoints.forms.usuario import UsuarioRegistration
from services import funcao_service, admin_service
from model.models import User, Funcionario
from app_util import create_system_user

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/registrar', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def registrar_usuario():

	form = UsuarioRegistration()
	form.funcao.choices = [(funcao.id, funcao.name.capitalize()) for funcao in funcao_service.query_funcoes()]
	if request.method == 'GET':
		return render_template('admin/admin/cadastrar_usuario.html', form=form)
	elif request.method == 'POST':

		# print(dir(form))
		if form.validate_on_submit():
			obj_dict = handle_form_user_registration(form)
			admin_service.new_user_handler(obj_dict['usuario'], obj_dict['funcionario'], form.data.funcao)
		else:
			return render_template('admin/admin/cadastrar_usuario.html', form=form)

def handle_form_user_registration(form):
	from flask.ext.security.utils import encrypt_password
	
	funcionario = Funcionario(nome=form.data.nome, sobrenome=form.data.sobrenome, telefone_residencial=form.data.numero_residencial,
		telefone_celular=form.data.numero_celular, cargo=form.cargo.data, data_admissao=date.today())
	username = create_system_user(funcionario.nome, funcionario.sobrenome)
	usuario = User(email=form.email.data, username=username, password=encrypt_password(password))

	return {'funcionario': funcionario, 'usuario': usuario}
