from models.cep_model import CepModel
import app_util.cep_request as viacep
import app_util.db as db

def cep_handler(cep_from_client):

	num_cep = cep_from_client.replace('-', '')

	cep = CepModel.query_by_id(num_cep)

	if cep is None:
		return viacep.get_cep(num_cep)

	return cep

def query_cep_by_id(cep):

	conn, cr = db.get_db_resources()

	try:
		cr.callproc('prc_get_cep_by_id', (cep,))
	except:
		raise
	else:
		cep = cr.fetchone()
	finally:
		cr.close()
		conn.close()

	return db_to_model(cep)

def db_to_model(db_row):

	return CepModel(db_row[0], db_row[1], db_row[2], db_row[3], db_row[4], db_row[5])