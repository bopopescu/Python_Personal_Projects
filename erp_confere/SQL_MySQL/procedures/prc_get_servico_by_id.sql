DELIMITER $$

USE erp $$

DROP PROCEDURE IF EXISTS prc_get_servico_by_id $$

CREATE PROCEDURE prc_get_servico_by_id(p_cd_servico INT)
BEGIN 
	
	SELECT * FROM servico WHERE cd_servico = p_cd_servico;

END $$


DELIMITER ;