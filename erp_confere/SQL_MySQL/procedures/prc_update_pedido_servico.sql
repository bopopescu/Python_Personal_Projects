DELIMITER $$


USE erp $$

DROP PROCEDURE IF EXISTS prc_update_pedido_servico $$

CREATE PROCEDURE prc_update_pedido_servico(p_cd_pedido INT, p_cd_servico INT,  p_cd_funcionario INT, p_vl_comissao DECIMAL(10,2), 
	p_dt_inicio DATE, p_dt_fim DATE, p_servico_props JSON)
COMMENT 'Update pedido_servico table using cd_pedido_servico as an argument'
BEGIN

	UPDATE
		erp.pedido_servico
	SET 
		cd_funcionario = p_cd_funcionario,
		vl_comissao = p_vl_comissao,
		dt_inicio = p_dt_inicio,
		dt_fim = p_dt_fim,
		servico_props = p_servico_props
	WHERE
		cd_pedido = p_cd_pedido
	AND
		cd_servico = p_cd_servico;

END $$


DELIMITER $$