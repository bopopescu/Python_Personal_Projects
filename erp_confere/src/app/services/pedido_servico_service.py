import app_util.db as db
import app_util.constants as const
from models.pedido_servico_model import PedidoServicoModel  
import app_util.json_util as json_util

def insert_pedido_servico(pedido_servico):
	pass


def json_to_model(pedido, servico):

	status = json_util.dict_to_str({'status': 'novo'})

	return PedidoServicoModel(pedido, servico, None, None, 0, None, status)


def update_pedido_servico(pedido_servico):

	conn, cr = db.get_db_resources()

	props = json_util.dict_to_str(pedido_servico['props'])

	cr.execute('call prc_update_pedido_servico(%s, %s, %s, %s, %s, %s)', 
		(pedido_servico['codigo'], pedido_servico['funcionario']['codigo'], 
		pedido_servico['valor_comissao'], pedido_servico['data_inicio'], pedido_servico['data_fim'],
		props))

	conn.commit()

	conn.close()