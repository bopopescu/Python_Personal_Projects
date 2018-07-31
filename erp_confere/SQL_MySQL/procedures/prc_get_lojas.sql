DELIMITER $$

USE erp $$

DROP PROCEDURE IF EXISTS prc_get_lojas $$

CREATE PROCEDURE prc_get_lojas()
COMMENT 'Get all the rows from loja table'
BEGIN
	
	SELECT * FROM loja;

END $$


DELIMITER ;