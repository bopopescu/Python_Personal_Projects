import app_util.db as db
import app_util.constants as const


class AmbienteModel(object):

	def __init__(self, codigo, nome):

		self.codigo = codigo
		self.nome = nome

	