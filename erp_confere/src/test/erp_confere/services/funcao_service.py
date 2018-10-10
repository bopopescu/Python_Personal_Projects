from model import Role 

def query_funcoes():
	return Role.query.all()

