DELIMITER $$

USE erp $$

DROP PROCEDURE IF EXISTS prc_get_previous_status_pedido_servico $$

CREATE PROCEDURE prc_get_previous_status_pedido_servico(p_cd_pedido INT, p_cd_servico INT, 
	OUT p_out_previous_status VARCHAR(40))
COMMENT 'Get the previous service state of the given pedido_servico'
BEGIN
	
	SELECT
		previous_status
	INTO
		p_out_previous_status
	FROM
		(
			SELECT
				ps.cd_servico,
				lag(ps.servico_props ->> '$.status') over window_f as previous_status 
			FROM	
				erp.pedido_servico ps
			    INNER JOIN
					erp.servico s
			        ON
						ps.cd_servico = s.cd_servico
			WHERE 
				ps.cd_pedido = p_cd_pedido
			WINDOW window_f AS (ORDER BY s.nr_sequencia)
		) AS sub_query
	WHERE
		sub_query.cd_servico = p_cd_servico;

END $$

DELIMITER ;
