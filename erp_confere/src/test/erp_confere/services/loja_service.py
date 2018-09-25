from model.models import Loja
from persistence.mysql_persistence import db

def query_all_lojas():
	return Loja.query.all()

def query_loja_by_id(codigo):
	return Loja.query.filter_by(codigo=codigo).first()

def insert_loja(loja):
	db.session.add(loja)
	db.session.commit()