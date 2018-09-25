from wtforms import DecimalField, StringField, SubmitField, validators
from flask_wtf import FlaskForm
from app_util import CustomDecimalField

class LojaCadastrarForm(FlaskForm):

	nome = StringField('Nome da Loja', [validators.DataRequired()])
	comissao_paga = CustomDecimalField("Valor da comissão (em %)", [validators.DataRequired()], places=2,rounding=None)
	enviar = SubmitField('Registrar')
