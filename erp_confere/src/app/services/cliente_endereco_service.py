import services.cep_service as cep_service
import services.cliente_service as cliente_service
from models.cliente_endereco_model import ClienteEnderecoModel
from models.cep_model import CepModel
from models.cliente_model import ClienteModel

def cliente_endereco_handler(dic):

	if 'endereco' in dic and 'cliente' in dic:
		
		numero_endereco = dic['endereco']['numero']
		complemento = dic['endereco']['complemento']
		referencia = dic['endereco']['referencia'] if 'referencia' in dic['endereco'] else None
		numero_cep = dic['endereco']['cep']
		
		cep = cep_service.cep_handler(numero_cep)
		cliente = cliente_service.cliente_handler(dic['cliente'])

		cliente_endereco = ClienteEnderecoModel.query_by_id(cep.cep, cliente.codigo)

		if cliente_endereco:
			# Change the int and str type for objs in both queries
			cliente_endereco.cep = CepModel.query_by_id(cliente_endereco.cep)
			cliente_endereco.cliente = ClienteModel.query_by_id(cliente_endereco.cliente) 

			return cliente_endereco

		cliente_endereco = ClienteEnderecoModel(cep, cliente, numero_endereco, 
				complemento, referencia)

		cliente_endereco.insert()

		return cliente_endereco
	else:
		return None