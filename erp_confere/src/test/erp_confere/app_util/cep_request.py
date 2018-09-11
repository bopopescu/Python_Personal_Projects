import requests
from model.models import Cep
import app_util.constants as const

VIACEP_URL = 'https://viacep.com.br/ws/:cep:/json/'

def get_cep(cep):
	base_url = VIACEP_URL.replace(':cep:', cep)
	response = requests.get(base_url)
	
	if response.status_code == 404:
		return None

	returned_cep = response.json()
	new_cep = Cep(numero=returned_cep['cep'].replace('-',''), logradouro=returned_cep['logradouro'], complemento=returned_cep['complemento'], 
		bairro=returned_cep['bairro'], cidade=returned_cep['localidade'], uf=returned_cep['uf'])

	return new_cep
