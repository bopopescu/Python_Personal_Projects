DELIMITER $$

USE erp $$

DROP PROCEDURE IF EXISTS prc_get_servicos $$

CREATE PROCEDURE prc_get_servicos()
COMMENT 'Query all rows available in servicos table'
BEGIN
	
	SELECT * FROM servico;

END $$


DELIMITER ;