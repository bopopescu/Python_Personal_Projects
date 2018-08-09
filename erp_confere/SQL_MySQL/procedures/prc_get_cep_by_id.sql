DELIMITER $$


USE erp $$

DROP PROCEDURE IF EXISTS prc_get_cep_by_id $$

CREATE PROCEDURE prc_get_cep_by_id(p_cep CHAR(8))
COMMENT 'Query cep table by cep as an argument'
BEGIN

	SELECT
		*
	FROM
		erp.cep
	WHERE
		cep = p_cep;

END $$


DELIMITER ;
