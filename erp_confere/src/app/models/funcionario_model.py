import app_util.db as db
import app_util.constants as const


class FuncionarioModel(object):

	def __init__(self, codigo, nome, sobrenome, data_admissao, data_demissao, 
		telefone_residencial, telefone_celular, cargo):

		self.codigo = codigo
		self.nome = nome
		self.sobrenome = sobrenome
		self.data_admissao = data_admissao
		self.data_demissao = data_demissao
		self.telefone_residencial = telefone_residencial
		self.telefone_celular = telefone_celular
		self.cargo = cargo

	@classmethod
	def query_by_id(cls, _id):
		pass
		