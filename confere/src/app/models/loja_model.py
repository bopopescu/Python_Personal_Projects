from db import db

class LojaModel(db.Model):

	__tablename__ = 'loja'

	_id = db.Column('cd_loja',db.Integer, primary_key=True)
	nome = db.Column('nm_loja', db.String(45))
	valor_comissao = db.Column('vl_comissao', db.Float(10,2))

	def __init__(self, nome, valor_comissao):
		self.nome = nome
		self.valor_comissao = valor_comissao

	@classmethod
	def find_by_id(cls, _id):
		return cls.query.filter_by(cd_loja=_id).first()
		
	def save_to_db(self):
		db.session.add(self)
		db.session.commit()
