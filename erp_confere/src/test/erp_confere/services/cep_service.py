from model import Cep
import app_util.cep_request as viacep
from persistence import db


def cep_handler(cep_from_client):

	num_cep = cep_from_client.replace('-', '')

	cep = query_cep_by_id(num_cep)

	if cep is None:
		new_cep = viacep.get_cep(num_cep)
		
		db.session.add(new_cep)
		db.session.commit()
		return new_cep

	return cep

def query_cep_by_id(cep):
	return Cep.query.filter_by(numero=cep).first()

def insert_cep(cep):
	db.session.add(cep)
	db.session.commit()
	db.session.close()
