from model import Funcionario, User, RolesUsers
from services import role_service
from persistence import db
from app_util import password_generator

def new_user_handler(user, funcionario, role_id):
	
	try:
		role = role_service.query_role_by_id(role_id)
		user.roles = [role]
		user.funcionario = funcionario
		new_pass = password_generator()
		user.password = new_pass
		db.session.add(user)
		db.session.add(funcionario)
		
	except Exception as e:
		raise
	else:
		db.session.commit()
	finally:
		db.session.close()


def query_usuarios():
	return User.query.all()


def query_usuario_by_id(user_id):
	return User.query.filter_by(id=user_id).one()
