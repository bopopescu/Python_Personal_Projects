import app_util.db as db
import app_util.constants as const

class ClienteEnderecoModel(object):

	def __init__(self, codigo, cep, cliente, numero_endereco, complemento,
		referencia):

		self.codigo = codigo
		self.cep = cep
		self.cliente = cliente
		self.numero_endereco = numero_endereco
		self.complemento = complemento
		self.referencia = referencia

	def insert(self, cursor):

		params = [self.codigo, self.cep.cep, self.cliente.codigo, self.numero_endereco,
			self.complemento, self.referencia]
		cursor.callproc('prc_insert_cliente_endereco', params)
		cursor.execute('SELECT @_prc_insert_cliente_endereco_0')
		self.codigo = cursor.fetchone()[0]

	@classmethod
	def query_by_id(cls, cep, codigo_cliente):

		conn, cr = db.get_db_resources()
		try: 
			cr.callproc('prc_get_cliente_endereco_by_cep_cliente', (cep, codigo_cliente))
		except:
			raise
		else:
			cliente_endereco = cr.fetchone()
		finally:
			cr.close()
			conn.close()

		if cliente_endereco:
			return cls(cliente_endereco[0], cliente_endereco[1], cliente_endereco[2], cliente_endereco[3],
				cliente_endereco[4], cliente_endereco[5])

		return None