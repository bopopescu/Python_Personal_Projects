DELIMITER $$

USE erp $$

DROP PROCEDURE IF EXISTS prc_get_funcionarios $$

CREATE PROCEDURE prc_get_funcionarios()
COMMENT 'Get all rows from funcionario table'
BEGIN

	SELECT * FROM funcionario;

END $$

DELIMITER ;