DELIMITER $$

USE erp $$

DROP PROCEDURE IF EXISTS prc_get_funcionario_by_id $$

CREATE PROCEDURE prc_get_funcionario_by_id(p_cd_funcionario INT)
BEGIN
	
	SELECT * FROM funcionario WHERE cd_funcionario = p_cd_funcionario;
	
END $$

DELIMITER ;