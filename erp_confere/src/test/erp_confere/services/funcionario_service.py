from persistence.mysql_persistence import db
from model.models import Funcionario

def query_funcionario_by_id(codigo_funcionario): 
	return Funcionario.query.filter_by(codigo_funcionario).first()

def query_funcionarios():
	return Funcionario.query.all()