from flask_security.forms import ChangePasswordForm
from wtforms import PasswordField, SubmitField ,validators

class CustomizedChangePasswordForm(ChangePasswordForm):
	password = PasswordField('Senha', [validators.DataRequired()])
	new_password = PasswordField('Nova Senha', [validators.DataRequired(),
						validators.EqualTo('new_password_confirm', message="Deve ser igual a confirmação"), 
				validators.Length(min=8,message="Senha deve conter no mínimo 8 caracteres")])
	new_password_confirm = PasswordField('Confirmar Nova Senha', [validators.DataRequired(), 
		validators.Length(min=8,message="Deve ter o mínimo de 8 caracteres")])
	change_password = SubmitField('Trocar')