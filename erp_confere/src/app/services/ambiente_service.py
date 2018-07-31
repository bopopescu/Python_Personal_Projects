from app_util import db
from models.ambiente_model import AmbienteModel

def get_all_ambientes():
	conn, cr = db.get_db_resources()

	cr.execute('CALL prc_get_ambientes()')
	results = cr.fetchall()

	ambientes = [AmbienteModel(row[0], row[1]) for row in results]

	cr.close()
	conn.close()

	return ambientes

