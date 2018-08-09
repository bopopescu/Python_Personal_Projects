DELIMITER $$


USE erp $$

DROP PROCEDURE IF EXISTS prc_get_cliente_endereco_by_id $$

CREATE PROCEDURE prc_get_cliente_endereco_by_id(p_cd_cliente_endereco INT)
COMMENT 'Query cliente_endereco table by ID'
BEGIN

	SELECT
		*
	FROM
		erp.cliente_endereco
	WHERE
		cd_cliente_endereco = p_cd_cliente_endereco;

END $$


DELIMITER ;
