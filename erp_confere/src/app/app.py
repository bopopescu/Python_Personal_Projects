from models.loja_model import LojaModel
from models.servico_model import ServicoModel

servico = ServicoModel.get_by_id(1)

servico.valor = 2

servico.update()
