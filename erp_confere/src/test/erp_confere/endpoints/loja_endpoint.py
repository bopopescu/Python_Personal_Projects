from flask import Blueprint, Flask, render_template, flash, request, redirect, url_for
from flask_security import login_required, roles_accepted
from endpoints.forms.loja_form import LojaCadastrarForm
from model.models import Loja
from services import loja_service

bp = Blueprint('loja', __name__, url_prefix='/loja')

@bp.route('/cadastrar', methods=['GET','POST'])
@login_required
@roles_accepted('admin', 'controladora')
def cadastrar():

	form = LojaCadastrarForm()

	if request.method == 'GET':
		return render_template('loja/cadastrar.html', form=form)
	elif request.method == 'POST':
		if form.validate_on_submit():
			new_loja = create_loja(form)
			loja_service.insert_loja(new_loja)
			flash('Loja criada com sucesso', 'success')
		else:
			flash(form.errors, 'error')

	db.session.close()
		
		return redirect(url_for('loja.cadastrar'))

@bp.route('/lojas', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def lojas():

	lojas = loja_service.query_all_lojas()
	return render_template('loja/loja.html', lojas=lojas)



def create_loja(form):
	return Loja(nome=form.data['nome'],valor_comissao=form.data['comissao_paga'])