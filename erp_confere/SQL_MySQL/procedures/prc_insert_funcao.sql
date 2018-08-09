DELIMITER $$

USE erp $$

DROP PROCEDURE IF EXISTS prc_insert_funcao $$

CREATE PROCEDURE prc_insert_funcao(OUT p_cd_funcao INT, p_nm_funcao VARCHAR(45))
COMMENT 'Insert a new entry in funcao table'
BEGIN

	
	INSERT INTO funcao (nm_funcao) VALUES (p_nm_funcao);

	SET p_cd_funcao = LAST_INSERT_ID();

END $$


DELIMITER ;