

class ClienteEnderecoModel():

	def __init__(self, cep, cliente, numero_endereco, complemento,
		referencia):

		self.cep = cep
		self.cliente = cliente
		self.numero_endereco = numero_endereco
		self.complemento = complemento
		self.referencia = referencia


	def insert(self):

		