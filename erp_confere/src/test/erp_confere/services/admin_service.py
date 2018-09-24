from model.models import Funcionario, User
from run import user_datastore
from services import role_service
from persistence.mysql_persistence import db

def new_user_handler(user, funcionario, role_id):
	role = role_service.query_role_by_id(role_id)
	user_datastore.add_role_to_user(user, role)

	funcionario.codigo = user.id
	db.session.add(funcionario)
	db.session.commit()









