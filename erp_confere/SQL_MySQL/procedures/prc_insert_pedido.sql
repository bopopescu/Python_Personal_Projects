DELIMITER $$

USE erp $$

DROP PROCEDURE IF EXISTS prc_insert_pedido $$

CREATE PROCEDURE prc_insert_pedido(OUT p_cd_pedido INT, p_cep CHAR(8), p_cd_cliente INT, p_cd_loja INT, p_cd_pedido_pai INT,
	p_nr_pedido VARCHAR(20), p_vl_pedido DECIMAL(10,2), p_dt_entrada DATE, p_dt_inicio DATE, p_dt_fim DATE, p_ambientes JSON)
COMMENT 'insert a new entry into pedido table'
BEGIN 
	
	INSERT INTO pedido (
		cep,
		cd_cliente,
		cd_loja,
		cd_pedido_pai,
		nr_pedido,
		vl_pedido,
		dt_entrada,
		dt_inicio,
		dt_fim,
		ambientes
	) VALUES (
		p_cep,
		p_cd_cliente,
        p_cd_loja,
		p_cd_pedido_pai,
		p_nr_pedido,
		p_vl_pedido,
		p_dt_entrada,
		p_dt_inicio,
		p_dt_fim,
		p_ambientes
	);

	SET p_cd_pedido = LAST_INSERT_ID();

END $$


DELIMITER ;