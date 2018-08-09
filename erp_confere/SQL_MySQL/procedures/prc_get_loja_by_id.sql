DELIMITER $$ 

USE erp $$

DROP PROCEDURE IF EXISTS prc_get_loja_by_id $$

CREATE PROCEDURE prc_get_loja_by_id(p_cd_loja INT)
COMMENT 'Get a row by id from loja table'
BEGIN

	SELECT * FROM loja WHERE cd_loja = p_cd_loja;

END $$


DELIMITER ;