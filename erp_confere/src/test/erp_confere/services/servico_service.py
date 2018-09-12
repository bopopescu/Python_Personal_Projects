from model.models import Servico
from persistence.mysql_persistence import db

def servico_handler(dic):
	pass

def query_servicos(servicos_list):	
	return Servico.query.filter(Servico.codigo.in_((servicos_list))).all()

def query_all_servicos():
	return Servico.query.all()

def query_servico_by_id(codigo_servico):
	return Servico.query.filter_by(codigo=codigo_servico).first()