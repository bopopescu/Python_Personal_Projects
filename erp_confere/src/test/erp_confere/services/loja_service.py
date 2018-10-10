from model import Loja
from persistence import db

def query_all_lojas():
	return Loja.query.all()

def query_loja_by_id(codigo):
	return Loja.query.filter_by(codigo=codigo).first()

def insert_loja(loja):
	db.session.add(loja)
	db.session.commit()


def query_loja_codigo_nome():
	return db.session.query(Loja)\
			.with_entities(Loja.codigo, Loja.nome)\
			.all()