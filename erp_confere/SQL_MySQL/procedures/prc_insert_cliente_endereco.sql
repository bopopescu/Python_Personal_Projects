DELIMITER $$

USE erp $$

DROP PROCEDURE IF EXISTS prc_insert_cliente_endereco $$

CREATE PROCEDURE prc_insert_cliente_endereco(OUT p_cd_cliente_endereco INT, p_cep CHAR(8), p_cd_cliente INT, 
	p_nr_endereco INT, p_ds_complemento VARCHAR(120))
COMMENT 'insert a new row into cliente_endereco_table'
BEGIN

	INSERT INTO cliente_endereco (
		 cep,
		 cd_cliente,
		 nr_endereco,
		 ds_complemento
	) VALUES (
		p_cep,
		p_cd_cliente,
		p_nr_endereco,
		p_ds_complemento
	);

	SET p_cd_cliente_endereco = LAST_INSERT_ID();

END $$


DELIMITER ;