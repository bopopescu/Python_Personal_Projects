from models.cliente_model import ClienteModel
import app_util.db as db
import app_util.constants as const
import MySQLdb as mysql

def cliente_handler(dic):

	cliente = verify_cliente(dic)
	if cliente:
		return cliente

	# If it doesn't exist, transforms the dictionary into ClienteModel object
	cliente = cliente_to_model(dic)
	insert_cliente(cliente)

	return cliente

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

def insert_cliente(cliente):
	conn = db.get_connection()
	cx = conn.cursor()

	try:
		cx.execute(const.INSERT_CLIENTE, (cliente.nome, cliente.sobrenome, cliente.email, 
			cliente.residencial, cliente.celular))
	except mysql.Error as e:
		conn.rollback()
	else:
		conn.commit()
	finally:
		cx.close()
		conn.close()