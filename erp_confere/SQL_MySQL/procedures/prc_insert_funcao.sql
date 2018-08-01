DELIMITER $$

USE erp $$

DROP PROCEDURE IF EXISTS prc_insert_funcao $$

CREATE PROCEDURE prc_insert_funcao(p_nm_funcao VARCHAR(45))
COMMENT 'Insert a new entry in funcao table'
BEGIN

	INSERT INTO funcao (nm_funcao) VALUES (p_nm_funcao);

END $$


DELIMITER ;