from models.servico_model import ServicoModel

def servico_handler(dic):
	pass

def get_servicos(servicos_list):
	servicos_to_search = [servico['codigo'] for servico in servicos_list]
	
	return ServicoModel.get_in_id(servicos_to_search)

