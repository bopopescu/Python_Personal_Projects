from model.models import Feriado
from persistence.mysql_persistence import db

def query_feriado_by_data(data_corrente):
	return Feriado.query.filter_by(data = data_corrente).all()


def query_feriados_to_come(data_corrente, limit_value=10):
	feriados = db.session.query(Feriado)\
			.with_entities(Feriado.data_feriado)\
			.filter(Feriado.data_feriado >= data_corrente)\
			.order_by(Feriado.data_feriado.asc())\
			.limit(limit_value)\
			.all()

	return [feriado[0] for feriado in feriados]
