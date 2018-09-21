from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SelectField, validators
import services.funcao_service as funcao_service


class UsuarioRegistration(FlaskForm):
	nome = StringField('Nome', [validators.length(max=45), validators.DataRequired()])
	sobrenome  = StringField('Sobrenome', [validators.length(max=45), validators.DataRequired()])
	senha = PasswordField('Senha', [validators.length(max=50), validators.DataRequired()])
	confirmar_senha = PasswordField('Confirmar senha', [validators.length(max=50), validators.DataRequired(),
		validators.EqualTo('senha', message="Senhas devem ser iguais")])
	email = StringField('Email', [validators.Email(), validators.DataRequired()])
	funcao = SelectField('Funcão', [validators.DataRequired()])

