DELIMITER $$


USE erp $$

DROP PROCEDURE IF EXISTS prc_get_cliente_endereco_by_cep_cliente $$

CREATE PROCEDURE prc_get_cliente_endereco_by_cep_cliente(p_cep CHAR(8), p_cd_cliente INT)
COMMENT 'Query cliente_endereco table by cep and cd_cliente as arguments'
BEGIN

	SELECT
		*
	FROM
		erp.cliente_endereco
	WHERE
		cep = p_cep
	AND 
		p_cd_cliente = p_cd_cliente;

END $$


DELIMITER ;
