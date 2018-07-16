DELIMITER $$


USE erp $$

DROP PROCEDURE IF EXISTS prc_get_pedido_by_id $$

CREATE PROCEDURE prc_get_pedido_by_id(p_cd_pedido INT)
COMMENT 'Query pedido table using cd_pedido arguments'
BEGIN
	SELECT 
		* 
	FROM 
		pedido 
	WHERE
		 cd_pedido = p_cd_pedido;
END $$

DELIMITER ;