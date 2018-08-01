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
