DELIMITER $$

USE erp $$

DROP PROCEDURE IF EXISTS prc_get_pedido_servico_by_servico $$

CREATE PROCEDURE prc_get_pedido_servico_by_pedido(p_cd_pedido INT)
COMMENT 'Get all pedido_servico from a specific cd_pedido'
BEGIN
	
	SELECT
		*
	FROM
		pedido_servico
	WHERE
		cd_pedido = p_cd_pedido;

END $$

DELIMITER ;