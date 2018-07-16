QUERY_LOJA_ALL = "SELECT * FROM loja"
QUERY_LOJA_BY_ID = "SELECT * FROM loja WHERE cd_loja = %s"
INSERT_LOJA = "INSERT INTO loja (nm_loja, vl_comissao) VALUES(%s,%s)"
UPDATE_LOJA = "UPDATE loja SET nm_loja = %s, vl_comissao = %s WHERE cd_loja = %s"

QUERY_SERVICO_BY_ID = "SELECT * FROM servico WHERE cd_servico = %s"
UPDATE_SERVICO = "UPDATE servico SET nm_servico = %s, vl_servico = %s, nr_sequencia = %s, tp_vl_servico = %s WHERE cd_servico = %s"
QUERY_SERVICO_IN_ID = "SELECT * FROM servico WHERE cd_servico IN (%s)"



FUNCAO_LOJA_BY_ID = "SELECT * FROM funcao WHERE cd_funcao = %s"
INSERT_FUNCAO = "INSERT INTO funcao (nome) VALUES(%s)"


CLIENTE_BY_ID = "SELECT cd_cliente, nm_cliente, sobre_nm_cliente, ds_email, nr_telefone_res, nr_telefone_cel " +\
	"FROM cliente WHERE cd_cliente = %s"
CLIENTE_BY_NOME = "SELECT cd_cliente, nm_cliente, sobre_nm_cliente, ds_email, nr_telefone_res, nr_telefone_cel" + \
		 " FROM cliente WHERE client_key = SHA2(CONCAT(TRIM(%s), TRIM(%s)), 256)"
INSERT_CLIENTE = "INSERT INTO cliente (nm_cliente, sobre_nm_cliente, ds_email, nr_telefone_res, nr_telefone_cel)" + \
				" VALUES (%s, %s, %s, %s, %s)"

QUERY_CEP_BY_ID = "SELECT * FROM cep WHERE cep = %s"
INSERT_CEP = "INSERT INTO cep (cep, logradouro, complemento, bairro, cidade, uf) VALUES(%s, %s, %s ,%s, %s, %s)"


QUERY_USUARIO_BY_ID = "SELECT u.cd_usuario, u.ds_username, u.ds_password, u.dt_criacao, u.dt_alteracao, f.nm_funcao" + \
		" FROM usuario u INNER JOIN funcao f ON u.cd_funcao = f.cd_funcao WHERE u.cd_usuario = %s"
QUERY_USUARIO_BY_USERNAME = "SELECT u.cd_usuario, u.ds_username, u.ds_password, u.dt_criacao, u.dt_alteracao, f.nm_funcao" + \
		" FROM usuario u INNER JOIN funcao f ON u.cd_funcao = f.cd_funcao WHERE u.ds_username = %s"
INSERT_USUARIO = "INSERT INTO usuario (cd_usuario, ds_username, ds_password, dt_criacao, dt_alteracao, cd_funcao) " + \
			"VALUES(%s, %s, %s ,%s, %s, %s)"



QUERY_FUNCIONARIO_BY_ID = "SELECT * FROM funcionario WHERE cd_funcionario = %s"
INSERT_FUNCIONARIO = "INSERT INTO funcionario (cd_funcionario, nm_funcionario, sobre_nm_funcionario, dt_admissao, dt_demissao, nr_telefone_res, nr_telefone_cel, ds_cargo) " + \
	"VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"


INSERT_CLIENTE_ENDERECO = "INSERT INTO cliente_endereco (cep, cd_cliente, nr_endereco, ds_complemento, ds_referencia) VALUES " + \
	"(%s,%s,%s,%s,%s)"
SELECT_CLIENTE_ENDERECO = "SELECT * FROM cliente_endereco WHERE cep = %s AND cd_cliente = %s"



INSERT_PEDIDO = "INSERT INTO pedido(cd_pedido, cep, cd_cliente, cd_loja, cd_pedido_pai, nr_pedido, vl_pedido, dt_entrada, dt_inicio, dt_fim, ambientes)" + \
	" VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"



INSERT_PEDIDO_SERVICO = "INSERT INTO pedido_servico(cd_pedido, cd_servico, cd_funcionario, dt_inicio,  vl_comissao, dt_fim, servico_props) " + \
	" VALUES (%s,%s,%s,%s,%s,%s,%s)" 
UPDATE_PEDIDO_SERVICO = "UPDATE pedido_servico SET cd_pedido = %s, cd_servico = %s, cd_funcionario = %s, vl_comissao = %s, dt_inicio = %s, dt_fim = %s, servico_props = %s "+\
"WHERE cd_pedido_serivco = %s" 
