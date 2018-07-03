from db import db 


class FuncaoModel(db.Model):

	__tablename__ = 'funcao'

	_id = db.Column('cd_funcao', db.Integer, primary_key=True)
	nome = db.Column('nm_funcao', db.String(40), nullable=False) 


	def __init__(self,nome):
		self.nome = nome

	@classmethod
	def find_by_name(cls,name):
		return cls.query.filter_by(nm_funcao=name).first()


	def save_to_db(self):
		db.session.add(self)
		db.session.commit()



