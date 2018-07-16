DELIMITER $$

USE erp $$

DROP PROCEDURE IF EXISTS prc_insert_pedido_servico $$

CREATE PROCEDURE prc_insert_pedido_servico(p_cd_pedido INT, p_cd_servico INT, p_cd_funcionario INT,
	p_vl_comissao DECIMAL(10,2), p_dt_inicio DATE, p_dt_fim DATE, p_servico_props JSON)
COMMENT 'insert in pedido_servico table a new row declaring all the fields'
BEGIN

	INSERT INTO
		pedido_servico (cd_pedido, cd_servico, cd_funcionario, vl_comissao, dt_inicio, dt_fim, servico_props)
	VALUES
		(p_cd_pedido, p_cd_servico, p_cd_funcionario, p_vl_comissao, p_dt_inicio, p_dt_fim, p_servico_props);

END $$

DELIMITER ;