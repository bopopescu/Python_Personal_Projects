from models.cliente_model import ClienteModel


def verify_cliente(dic):

	cliente = ClienteModel.query_by_name(dic['nome'], dic['sobrenome'])
	if cliente:
		return cliente

	return None

def cliente_to_model(dic):

	nome = dic['nome']
	sobrenome = dic['sobrenome']
	email = dic['email']
	residencial = dic['telefone_residencial'] if 'telefone_residencial' in dic else None
	celular = dic['telefone_celular'] 

	return ClienteModel(None, nome, sobrenome, email, residencial, celular)

def insert_cliente(dic):

	cliente = verify_cliente(dic)

	if cliente:
		return cliente

	# If it doesn't exist, transforms the dictionary into ClienteModel object
	cliente = cliente_to_model(dic)
	cliente.insert()

	return cliente
