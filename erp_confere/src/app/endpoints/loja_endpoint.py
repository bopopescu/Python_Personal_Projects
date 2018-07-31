from flask import Blueprint, Flask, render_template, flash, request, redirect, url_for


loja = Blueprint('loja', __name__, url_prefix='/loja')



@loja.route('/cadastrar', methods=['GET','POST'])
def cadastrar():

	if request.method == 'POST':

		print(request.form['nome'])
		print(request.form['valor_comissao'])

		message = "Successful"
		flash(message)

		return redirect(url_for('loja.cadastrar'))

	return render_template('loja/cadastrar.html')
