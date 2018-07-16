from models.cliente_model import ClienteModel
import app_util.db as db
import app_util.constants as const
import MySQLdb as mysql

def cliente_handler(dic):

	cliente = verify_cliente(dic)
	if cliente:
		return cliente

	# If it doesn't exist, transforms the dictionary into ClienteModel object
	cliente = json_to_model(dic)
	insert_cliente(cliente)

	return cliente

def verify_cliente(dic):

	cliente = ClienteModel.query_by_name(dic['nome'], dic['sobrenome'])
	if cliente:
		return cliente

	return None

def json_to_model(dic):

	nome = dic['nome']
	sobrenome = dic['sobrenome']
	email = dic['email']
	residencial = dic['telefone_residencial'] if 'telefone_residencial' in dic else None
	celular = dic['telefone_celular'] 

	return ClienteModel(None, nome, sobrenome, email, residencial, celular)

def insert_cliente(cliente):
	conn, cx = db.get_db_resources()
	
	try:
		cx.execute(const.INSERT_CLIENTE, (cliente.nome, cliente.sobrenome, cliente.email, 
			cliente.residencial, cliente.celular))
		cliente.codigo = cx.lastrowid
	except mysql.Error as e:
		conn.rollback()
	else:
		conn.commit()
	finally:
		cx.close()
		conn.close()


def query_cliente(nome, sobrenome):

	conn, cr = db.get_db_resources()

	cr.execute('call prc_get_cliente_by_name(%s, %s)', (nome, sobrenome))
	
	result_set = cr.fetchone()

	if result_set:
		cliente = db_to_model(result_set)
	else:
		cliente = result_set

	cr.close()
	conn.close()

	return cliente

def db_to_model(db_row):

	return ClienteModel(db_row[0], db_row[1], db_row[2], db_row[3], db_row[4], db_row[5])