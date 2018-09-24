from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SelectField, SubmitField, DecimalField, IntegerField, validators
import services.funcao_service as funcao_service


class UsuarioRegistration(FlaskForm):
	nome = StringField('Nome*', [validators.length(max=45), validators.DataRequired(message="Campo obrigatório")])
	sobrenome  = StringField('Sobrenome*', [validators.length(max=45), validators.DataRequired(message="Campo obrigatório")])
	senha = PasswordField('Senha*', [validators.length(min=8, max=50), validators.DataRequired(message="Campo obrigatório")])
	confirmar_senha = PasswordField('Confirmar senha*', 
		[validators.length(min=8, message="Senha com o mínimo de 8 caracteres"), 
		validators.DataRequired(message="Campo obrigatório"),
		validators.EqualTo('senha', message="Senhas devem ser iguais")])
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
