from persistence import db
from model import Funcionario
from sqlalchemy.orm.exc import NoResultFound

def query_funcionario_by_id(codigo_funcionario): 
	try:
		 funcionario = Funcionario.query.filter_by(codigo=codigo_funcionario).first()
	except NoResultFound as e:
		funcionario = None
	finally:
		return funcionario
	

def query_funcionarios():
	return Funcionario.query.all()