from db import db


class ItemModel(db.Model):

	# Table name
	__tablename__ = 'items'
	# Database columns
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	price = db.Column(db.Float(precision=10,scale=2))
	# Foreign key declaration
	store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

	# Class name which contains the relationship
	store = db.relationship('StoreModel')

	def __init__(self,name,price,store_id):
		self.name = name
		self.price = price
		self.store_id = store_id

	def json(self):
		return {'name': self.name, 'price': self.price, 'store_id': self.store_id}

	@classmethod
	def find_by_name(cls, name):
		# filter_by can be used as method chaining 
		return cls.query.filter_by(name=name).first()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()