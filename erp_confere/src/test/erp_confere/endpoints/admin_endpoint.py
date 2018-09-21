from flask import Blueprint, url_for, render_template, redirect, flash
from flask_security import login_required, roles_accepted, current_user
from endpoints.forms.usuario import UsuarioRegistration
from services import funcao_service

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/registrar')
@login_required
@roles_accepted('admin')
def registrar_usuario():
	form = UsuarioRegistration()
	form.funcao.choices = [(funcao.id, funcao.name.capitalize()) for funcao in funcao_service.query_funcoes()]
	return render_template('admin/admin/cadastrar_usuario.html', form=form)

