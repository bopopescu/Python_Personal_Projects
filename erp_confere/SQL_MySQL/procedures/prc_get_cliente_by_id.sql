DELIMITER $$

USE erp $$

DROP PROCEDURE IF EXISTS prc_get_cliente_by_id $$

CREATE PROCEDURE prc_get_cliente_by_id(p_cd_cliente INT)
COMMENT 'Query cliente table by cd_cliente as an argument'
BEGIN

	SELECT
		cd_cliente, 
		nm_cliente, 
		sobre_nm_cliente, 
		ds_email, 
		nr_telefone_res, 
		nr_telefone_cel
	FROM
		erp.cliente
	WHERE
		cd_cliente = p_cd_cliente;

END $$

DELIMITER ;