from wtforms import DecimalField, StringField, SubmitField, validators, \
BooleanField, SelectField, PasswordField, IntegerField, DateField
from flask_wtf import FlaskForm
from flask_security.forms import ChangePasswordForm
from app_util import CustomDecimalField
import services.funcao_service as funcao_service

class LojaCadastrarForm(FlaskForm):

	nome = StringField('Nome da Loja', [validators.DataRequired()])
	comissao_paga = CustomDecimalField("Valor da comissão (em %)", [validators.DataRequired()], places=2,rounding=None)
	enviar = SubmitField('Registrar')


class PedidoFilterForm(FlaskForm):

	filtrar_por = SelectField('Filtrar por', choices=[('', ''), ('loja', 'Loja'), ('status', 'Status')], default=None)
	loja_filtro = SelectField('Loja')
	status_filtro = SelectField('Status', choices=[('novo', 'Novo'), ('iniciado', 'Iniciado'), ('agendado', 'Agendado'), ('concluido', 'Concluído')], default=None)
	filtrar = SubmitField('Filtrar')


class PedidoServicoListaFiltroForm(FlaskForm):

	filtrar_por = SelectField('Filtrar por', choices=[('', ''), ('loja', 'Loja'), ('status', 'Status'), ('pedido_codigo', 'Código Pedido')])
	loja = SelectField('Loja')
	status = SelectField('Status', choices=[('novo', 'Novo'), ('agendado', 'Agendado'), ('iniciado', 'Iniciado'), ('concluido', 'Concluído'), 
		('liberado', 'Liberado'), ('atrasado', 'Atrasado')])
	pedido_codigo = StringField('Pedido', [validators.DataRequired(), validators.length(min=2)])
	filtrar = SubmitField('Filtrar')


class CustomizedChangePasswordForm(ChangePasswordForm):
	password = PasswordField('Senha', [validators.DataRequired()])
	new_password = PasswordField('Nova Senha', [validators.DataRequired(),
						validators.EqualTo('new_password_confirm', message="Deve ser igual a confirmação"), 
				validators.Length(min=8,message="Senha deve conter no mínimo 8 caracteres")])
	new_password_confirm = PasswordField('Confirmar Nova Senha', [validators.DataRequired(), 
		validators.Length(min=8,message="Deve ter o mínimo de 8 caracteres")])
	change_password = SubmitField('Trocar')


class UsuarioRegistration(FlaskForm):
	nome = StringField('Nome*', [validators.length(max=45), validators.DataRequired(message="Campo obrigatório")])
	sobrenome  = StringField('Sobrenome*', [validators.length(max=45), validators.DataRequired(message="Campo obrigatório")])
	email = StringField('Email*', [validators.Email(message="Endereço de e-mail inválido"), validators.DataRequired()])
	funcao = SelectField('Funcão no sistema*', [validators.DataRequired(message="Campo obrigatório")], coerce=int)
	submit = SubmitField('Registrar')
	numero_residencial = DecimalField('Telefone residencial', [validators.Optional()],
		places=None, rounding=None)
	numero_celular = DecimalField('Telefone celular*', [validators.DataRequired(message="Telefone Celuĺar é obrigatório")],
		places=None, rounding=None)
	cargo = SelectField('Cargo do funcionário*', [validators.DataRequired(message="Favor escolher o cargo do funcionário")], 
		choices=[('Socio', 'Sócio'), ('Finalizador', 'Finalizador'), ('Projetista', 'Projetista'),
		 ('Medidor', 'Medidor'), ('Secretaria', 'Secretária')])
	ativo = BooleanField('Ativo', [validators.DataRequired(message="Escolher se deve estar ativo ou não")])


class DashFilterForm(FlaskForm):
	'''
		Create a form to filter the date in flask form
	'''
	data_inicio = DateField('Data inicio', [validators.DataRequired(message="Favor informar a data início")], format="%Y-%m-%d")
	data_fim = DateField('Data fim', [validators.DataRequired(message="Favor informar a data início")], format="%Y-%m-%d")
	filtrar = SubmitField('Filtrar')
