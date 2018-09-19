from collections import namedtuple
from functools import partial

from flask.ext.login import current_user
from flask.ext.principal import identity_loaded, Pemission, RoleNeed, UserNeed

PedidoServicoNeed = namedtuple('pedido_servico', ['method', 'value'])
EditPedidoServicoNeed = partial(PedidoServicoNeed, 'atualizar')


class MedicaoPermissao(Permission):
	def __init__(self, codigo_servico):
		need_medicao = EditPedidoServicoNeed(codigo_servico)
		super().__init__(need_medicao)

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
	identity.user = curent_user