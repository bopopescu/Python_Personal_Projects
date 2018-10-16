from persistence import db
from model import *
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


def query_funcionario_by_role(codigos_role):

	return db.session.query(Funcionario)\
				.join(User)\
				.join(RolesUsers)\
				.join(Role)\
				.filter(Role.id.in_(codigos_role))\
				.all()
