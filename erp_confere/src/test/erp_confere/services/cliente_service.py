from model.models import Cliente
import app_util.constants as const
from persistence.mysql_persistence import db

def cliente_handler(dic):
	cliente = verify_cliente(dic)
	if cliente:
		return cliente

	cliente = json_to_model(dic)
	insert_cliente(cliente)
	return cliente

def verify_cliente(dic):
	cliente = ClienteModel.query_cliente_by_name(dic['nome'].strip(), dic['sobrenome'].strip())
	if cliente:
		return cliente
	return None

def json_to_model(dic):

	nome = dic['nome']
	sobrenome = dic['sobrenome']
	email = dic['email']
	residencial = dic['tel_residencial'] if 'tel_residencial' in dic and dic['tel_residencial'] != '' else None
	celular = dic['tel_celular']

	return Cliente(nome=nome, sobrenome=sobrenome, email=email, telefone_residencial=residencial, telefone_celular=celular)

def insert_cliente(cliente):
	db.session.add(cliente)
	db.session.commit()
	db.session.close()

def query_cliente_by_name(nome, sobrenome):
	return Cliente.query.filter_by(nome=nome, sobrenome=sobrenome).first()

def query_cliente_by_id(codigo):
	return Cliente.query.filter_by(codigo=codigo).first()