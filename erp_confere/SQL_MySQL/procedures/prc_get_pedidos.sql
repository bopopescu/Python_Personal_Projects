DELIMITER $$

USE erp $$

DROP PROCEDURE prc_get_pedidos $$

CREATE PROCEDURE prc_get_pedidos()
COMMENT 'Get all rows from pedido table '
BEGIN 
	
	SELECT * FROM pedido;

END $$

DELIMITER ;