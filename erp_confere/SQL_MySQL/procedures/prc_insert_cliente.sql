DELIMITER $$

USE erp $$

DROP PROCEDURE IF EXISTS prc_insert_cliente $$

CREATE PROCEDURE prc_insert_cliente(OUT p_cd_cliente INT, p_nm_cliente VARCHAR(45), p_sobre_nm_cliente VARCHAR(45)
	, p_email VARCHAR(80), p_nr_telefone BIGINT, p_nr_telefone_cel BIGINT)
COMMENT 'Insert a new row in cliente table'
BEGIN
	
	INSERT INTO cliente
		(nm_cliente, 
		sobre_nm_cliente, 
		ds_email, 
		nr_telefone_res, 
		nr_telefone_cel) 
	VALUE
		(TRIM(p_nm_cliente), 
		TRIM(p_sobre_nm_cliente), 
		TRIM(p_email), 
		p_nr_telefone, 
		p_nr_telefone_cel);

	SELECT LAST_INSERT_ID() INTO p_cd_cliente;

END 


DELIMITER ;