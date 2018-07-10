import requests
from models.cep_model import CepModel

VIACEP_URL = 'https://viacep.com.br/ws/:cep:/json/'

def get_cep(cep):

	base_url = VIACEP_URL.replace(':cep:', cep)
	response = requests.get(base_url)
	
	if response.status_code == 404:
		return None

	new_cep = cep_to_model(response.json())
	new_cep.insert()
	return new_cep


def cep_to_model(dict):

	cep = dict['cep'].replace('-', '')
	logradouro = dict['logradouro']
	complemento = dict['complemento']
	bairro = dict['bairro']
	cidade = dict['localidade']
	uf = dict['uf'] 

	return CepModel(cep, logradouro, complemento, bairro, cidade, uf)

