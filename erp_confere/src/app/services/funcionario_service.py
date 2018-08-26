import app_util.db as db
from models.funcionario_model import FuncionarioModel

def query_funcionario_by_id(codigo_funcionario): 

	conn, cr = db.get_db_resources()

	try:
		cr.callproc('prc_get_funcionario_by_id', (codigo_funcionario,))
	except:
		raise
	else:
		db_row = cr.fetchone()
	finally:
		cr.close()
		conn.close()

	if db_row:
		return FuncionarioModel(db_row[0],db_row[1],db_row[2],db_row[3],db_row[4],
			db_row[5],db_row[6],db_row[7])

	return None

def query_funcionarios():

	conn, cr = db.get_db_resources()

	try:
		cr.callproc('prc_get_funcionarios')
	except:
		raise
	else:
		db_rows = cr.fetchall()
	finally:
		cr.close()
		conn.close()

	funcionarios = [FuncionarioModel(db_row[0],db_row[1],db_row[2],db_row[3],db_row[4],db_row[5],db_row[6],db_row[7]) 
	for db_row in db_rows]

	return funcionarios