from models.loja_model import LojaModel
import app_util.db as db

def query_loja(codigo):

	loja = LojaModel.query_by_id(codigo)

	if loja:
		return loja
	else:
		raise ValueError('Loja não')

def query_all_lojas():

	conn, cr = db.get_db_resources()

	cr.execute('CALL prc_get_lojas()')
	rows = cr.fetchall()

	lojas = [LojaModel(row[0], row[1], row[2]) for row in rows]

	cr.close()
	conn.close()

	return lojas;


def query_loja_by_id(codigo):

	conn, cr = db.get_db_resources()

	try:
		cr.callproc('prc_get_loja_by_id', (codigo,))
	except:
		raise
	else:
		row = cr.fetchone()
	finally:
		cr.close()
		conn.close()

	return db_to_model(row)

def db_to_model(db_row):
	return LojaModel(db_row[0], db_row[1], db_row[2])