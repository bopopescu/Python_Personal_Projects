import requests
from models.cep_model import CepModel
import app_util.db as db
import app_util.constants as const
import MySQLdb as mysql

VIACEP_URL = 'https://viacep.com.br/ws/:cep:/json/'

def get_cep(cep):

	base_url = VIACEP_URL.replace(':cep:', cep)
	response = requests.get(base_url)
	
	if response.status_code == 404:
		return None

	new_cep = cep_to_model(response.json())

	insert_cep(new_cep)

	return new_cep

def cep_to_model(dict):

	cep = dict['cep'].replace('-', '')
	logradouro = dict['logradouro']
	complemento = dict['complemento']
	bairro = dict['bairro']
	cidade = dict['localidade']
	uf = dict['uf'] 

	return CepModel(cep, logradouro, complemento, bairro, cidade, uf)

def insert_cep(object_cep):
	conn = db.get_connection()

	cx = conn.cursor()
	try:	
		cx.execute(const.INSERT_CEP, (object_cep.cep, object_cep.logradouro, object_cep.complemento,
			object_cep.bairro, object_cep.cidade, object_cep.uf))
	except mysql.Error as e:
		conn.rollback()
		raise
	else:
		conn.commit()
	finally:
		cx.close()
		conn.close()