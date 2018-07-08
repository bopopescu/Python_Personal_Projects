QUERY_LOJA_ALL = "SELECT * FROM loja"
QUERY_LOJA_BY_ID = "SELECT * FROM loja WHERE cd_loja = %s"
INSERT_LOJA = "INSERT INTO loja (nm_loja, vl_comissao) VALUES(%s,%s)"
UPDATE_LOJA = "UPDATE loja SET nm_loja = %s, vl_comissao = %s WHERE cd_loja = %s"

QUERY_SERVICO_BY_ID = "SELECT * FROM servico WHERE cd_servico = %s"
UPDATE_SERVICO = "UPDATE servico SET nm_servico = %s, vl_servico = %s, nr_sequencia = %s, tp_vl_servico = %s WHERE cd_servico = %s"


FUNCAO_LOJA_BY_ID = "SELECT * FROM funcao WHERE cd_funcao = %s"
INSERT_FUNCAO = "INSERT INTO funcao (nome) VALUES(%s)"


CLIENTE_LOJA_BY_ID = "SELECT * FROM cliente WHERE cd_cliente = %s"
INSERT_CLIENTE = "INSERT INTO cliente (nm_cliente, sobre_nm_cliente, ds_email, nr_telefone_res, nr_telefone_cel)" + \
				" VALUES(%s, %s, %s, %s, %s)"

QUERY_CEP_BY_ID = "SELECT * FROM cep WHERE cd_cep = %s"
INSERT_CEP = "INSERT INTO cep (cep, logradouro, complemento, bairro, cidade, uf) VALUES(%s, %s, %s ,%s, %s, %s)"