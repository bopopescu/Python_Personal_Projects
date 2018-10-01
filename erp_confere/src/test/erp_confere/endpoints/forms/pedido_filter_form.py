from wtforms import SelectField, SubmitField
from flask_wtf import FlaskForm

class PedidoFilterForm(FlaskForm):

	filtrar_por = SelectField('Filtrar por', choices=[('', ''), ('loja', 'Loja'), ('status', 'Status')], default=None)
	loja_filtro = SelectField('Loja')
	status_filtro = SelectField('Status', choices=[('novo', 'Novo'), ('iniciado', 'Iniciado'), ('agendado', 'Agendado'), ('concluido', 'Concluído')], default=None)
	filtrar = SubmitField('Filtrar')
