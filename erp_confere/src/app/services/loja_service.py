from models.loja_model import LojaModel



def query_loja(loja):

	loja = LojaModel.query_by_id(loja['codigo'])

	if loja:
		return loja
	else:
		raise ValueError('Loja não')
