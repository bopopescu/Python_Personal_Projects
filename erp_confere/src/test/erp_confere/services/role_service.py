from model import Role

def query_role_by_id(role_id):
	return Role.query.filter_by(id=role_id).one()