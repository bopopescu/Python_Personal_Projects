DELIMITER $$

USE erp $$

DROP PROCEDURE IF EXISTS prc_get_cliente_by_name $$

CREATE PROCEDURE prc_get_cliente_by_name(p_nm_cliente VARCHAR(45), p_sobre_nm_cliente VARCHAR(80))
COMMENT 'Query cliente table by nm_cliente and sobre_nm_cliente as arguments. Selecting fields because client_key column is a internal column'
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
		client_key = SHA2(CONCAT(TRIM(p_nm_cliente), TRIM(p_sobre_nm_cliente)), 256);

END $$

DELIMITER ;
