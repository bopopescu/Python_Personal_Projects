DELIMITER $$

USE erp $$

DROP PROCEDURE IF EXISTS prc_get_pedido_servico_by_id $$

CREATE PROCEDURE prc_get_pedido_servico_by_id(p_cd_pedido INT, p_cd_servico INT)
COMMENT 'Query pedido_servico table using cd_pedido and cd_servico as arguments'
BEGIN

	SELECT 
		*
	FROM
		erp.pedido_servico
	WHERE
		cd_pedido = p_cd_pedido
	AND
		cd_servico = p_cd_servico;

END $$


DELIMITER ;