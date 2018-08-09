import services.cep_service as cep_service
import services.cliente_service as cliente_service
from models.cliente_endereco_model import ClienteEnderecoModel
from models.cep_model import CepModel
from models.cliente_model import ClienteModel
import app_util.db as db

def cliente_endereco_handler(dic):
		
		numero_endereco = dic['numero']
		complemento = dic['complemento'] if 'complemento' in dic else None
		referencia = dic['referencia'] if 'referencia' in dic else None
		numero_cep = dic['cep']

		cep, cliente = resolve_cep_cliente(numero_cep, dic)

		cliente_endereco = ClienteEnderecoModel.query_by_id(cep.cep, cliente.codigo)

		if cliente_endereco:
			# get the related objects from db
			cliente_endereco.cep = CepModel.query_by_id(cliente_endereco.cep)
			cliente_endereco.cliente = ClienteModel.query_by_id(cliente_endereco.cliente) 

			return cliente_endereco

		cliente_endereco = ClienteEnderecoModel(None, cep, cliente, numero_endereco, 
				complemento, referencia)

		conn, cx =  db.get_db_resources()
		try:
			cliente_endereco.insert(cx)
		except:
			raise
		else:
			conn.commit()
		finally:
			conn.close()
			cx.close()

		return cliente_endereco

def resolve_cep_cliente(numero_cep, dic):
	cep = cep_service.cep_handler(numero_cep)
	cliente = cliente_service.cliente_handler(dic)

	return cep, cliente


def query_cliente_endereco_by_id(codigo_cliente_endereco):

	conn, cr = db.get_db_resources()

	try:
		cr.callproc('prc_get_cliente_endereco_by_id', (codigo_cliente_endereco,))
	except:
		raise
	else:
		cliente_endereco = cr.fetchone()
	finally:
		cr.close()
		conn.close()

	return db_to_model(cliente_endereco)


def get_cliente_endereco(codigo_cliente_endereco):
		
	cliente_endereco = query_cliente_endereco_by_id(codigo_cliente_endereco)

	codigo_cliente = cliente_endereco.cliente
	cliente_endereco.cliente = cliente_service.query_cliente_by_id(codigo_cliente)

	numero_cep = cliente_endereco.cep
	cliente_endereco.cep = cep_service.query_cep_by_id(numero_cep)

	return cliente_endereco


def db_to_model(db_row):
	return ClienteEnderecoModel(db_row[0], db_row[1], db_row[2], db_row[3], db_row[4], db_row[5])