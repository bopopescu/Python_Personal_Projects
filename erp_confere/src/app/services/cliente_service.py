from models.cliente_model import ClienteModel


def verify_cliente(dic):

	cliente = ClienteModel.query_by_name(dic['nome'], dic['sobrenome'])

	if cliente:
		return cliente

	cliente = cliente_to_model(dic)
	cliente.insert()

	return cliente

def cliente_to_model(dic):

	nome = dic['nome']
	sobrenome = dic['sobrenome']
	email = dic['email']
	residencial = dic['telefone_residencial'] if 'telefone_residencial' in dic else None
	celular = dic['telefone_celular'] 

	return ClienteModel(None, nome, sobrenome, email, residencial, celular)