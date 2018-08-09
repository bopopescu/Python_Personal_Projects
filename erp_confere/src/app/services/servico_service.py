from models.servico_model import ServicoModel
from app_util import db

def servico_handler(dic):
	pass

def get_servicos(servicos_list):
	
	return ServicoModel.get_in_id(servicos_list)


def get_all_servicos():

	conn, cr = db.get_db_resources()
	cr.execute("CALL prc_get_servicos()")
	rows = cr.fetchall()

	servicos =  [ServicoModel(row[0], row[1], row[2], row[3], row[4]) for row in rows]

	cr.close()
	conn.close()

	return servicos

def query_servico_by_id(codigo_servico):

	conn, cr = db.get_db_resources()

	try:
		cr.callproc('prc_get_servico_by_id', (codigo_servico,))
	except:
		raise
	else:
		db_row = cr.fetchone()
	finally:
		cr.close()
		conn.close()

	return ServicoModel(db_row[0],db_row[1],db_row[2],db_row[3],db_row[4])	