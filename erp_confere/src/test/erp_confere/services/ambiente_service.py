from model.models import Ambiente

def query_all_ambientes():
	return Ambiente.query.all()

