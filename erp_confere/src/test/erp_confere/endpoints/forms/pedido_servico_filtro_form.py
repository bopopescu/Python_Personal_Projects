from wtforms import SubmitField, SelectField, StringField, validators
from flask_wtf import FlaskForm

class PedidoServicoListaFiltroForm(FlaskForm):

	filtrar_por = SelectField('Filtrar por', choices=[('', ''), ('loja', 'Loja'), ('status', 'Status'), ('pedido_codigo', 'Código Pedido')])
	loja = SelectField('Loja')
	status = SelectField('Status', choices=[('novo', 'Novo'), ('agendado', 'Agendado'), ('iniciado', 'Iniciado'), ('concluido', 'Concluído'), 
		('liberado', 'Liberado'), ('atrasado', 'Atrasado')])
	pedido_codigo = StringField('Pedido', [validators.DataRequired(), validators.length(min=2)])
	filtrar = SubmitField('Filtrar')
