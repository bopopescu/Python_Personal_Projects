import services.cep_service as cep_service
import services.cliente_service as cliente_service
from models.cliente_endereco_model import ClienteEnderecoModel
from models.cep_model import CepModel
from models.cliente_model import ClienteModel

def cliente_endereco_handler(dic):
		
		numero_endereco = dic['numero']
		complemento = dic['complemento'] if 'complemento' in dic else None
		referencia = dic['referencia'] if 'referencia' in dic else None
		numero_cep = dic['cep']
		
		cep = cep_service.cep_handler(numero_cep)
		cliente = cliente_service.cliente_handler(dic)

		cliente_endereco = ClienteEnderecoModel.query_by_id(cep.cep, cliente.codigo)

		if cliente_endereco:
			# get the related objects from db
			cliente_endereco.cep = CepModel.query_by_id(cliente_endereco.cep)
			cliente_endereco.cliente = ClienteModel.query_by_id(cliente_endereco.cliente) 

			return cliente_endereco

		cliente_endereco = ClienteEnderecoModel(cep, cliente, numero_endereco, 
				complemento, referencia)

		cliente_endereco.insert()

		return cliente_endereco
	