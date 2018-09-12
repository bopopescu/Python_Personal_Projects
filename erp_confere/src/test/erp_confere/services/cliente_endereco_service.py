import services.cep_service as cep_service
import services.cliente_service as cliente_service
from model.models import ClienteEndereco
from model.models import Cep
from model.models import Cliente
from persistence.mysql_persistence import db

def cliente_endereco_handler(dic):
		
		numero_endereco = dic['numero']
		complemento = dic['complemento'] if 'complemento' in dic else None
		referencia = dic['referencia'] if 'referencia' in dic else None
		numero_cep = dic['cep']

		cep, cliente = resolve_cep_cliente(numero_cep, dic)

		cliente_endereco = query_cliente_endereco_by_cep_cliente(cep.numero, cliente.codigo)

		if cliente_endereco:
			cliente_endereco.cep_obj = cep_service.query_cep_by_id(cliente_endereco.cep)
			cliente_endereco.cliente_obj = cliente_service.query_cliente_by_id(cliente_endereco.cliente) 

			return cliente_endereco

		cliente_endereco = ClienteEndereco(cep_obj=cep, cliente_obj=cliente, numero=numero_endereco, 
				complemento=complemento, referencia=referencia)

		insert_cliente_endereco(cliente_endereco)

		return cliente_endereco

def insert_cliente_endereco(cliente_endereco):
	db.session.add(cliente_endereco)
	db.session.commit()


def resolve_cep_cliente(numero_cep, dic):
	cep = cep_service.cep_handler(numero_cep)
	cliente = cliente_service.cliente_handler(dic)

	return cep, cliente

def query_cliente_endereco_by_cep_cliente(cep, cliente):
	return ClienteEndereco.query.filter_by(cep=cep, cliente=cliente).first()


def query_cliente_endereco_by_id(codigo_cliente_endereco):
	return ClienteEndereco.query.filter_by(codigo=codigo_cliente_endereco).first()


# def get_cliente_endereco(codigo_cliente_endereco):
		
# 	cliente_endereco = query_cliente_endereco_by_id(codigo_cliente_endereco)

# 	codigo_cliente = cliente_endereco.cliente
# 	cliente_endereco.cliente = cliente_service.query_cliente_by_id(codigo_cliente)

# 	numero_cep = cliente_endereco.cep
# 	cliente_endereco.cep = cep_service.query_cep_by_id(numero_cep)

# 	return cliente_endereco
