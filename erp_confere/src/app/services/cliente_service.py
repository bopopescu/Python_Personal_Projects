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
	residencial = dic['tel_residencial'] if 'tel_residencial' in dic and dic['tel_residencial'] != '' else None
	celular = dic['tel_celular']

	return ClienteModel(None, nome, sobrenome, email, residencial, celular)

def insert_cliente(cliente):
	conn, cx = db.get_db_resources()
	
	try:
		cx.callproc('prc_insert_cliente', (cliente.codigo, cliente.nome, cliente.sobrenome, 
			cliente.email, cliente.residencial, cliente.celular))
		cx.execute('SELECT @_prc_insert_cliente_0')
		cliente.codigo = cx.fetchone()[0]

		print(cliente.codigo)
	except mysql.Error as e:
		raise
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

def query_cliente_by_id(codigo):

	conn, cr = db.get_db_resources()

	try:
		cr.callproc('prc_get_cliente_by_id', (codigo,))
	except:
		raise
	else:
		cliente = cr.fetchone()
	finally:
		cr.close()
		conn.close()

	return db_to_model(cliente)

def db_to_model(db_row):

	return ClienteModel(db_row[0], db_row[1], db_row[2], db_row[3], db_row[4], db_row[5])