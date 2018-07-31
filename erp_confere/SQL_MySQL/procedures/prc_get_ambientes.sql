DELIMITER $$


USE erp $$

DROP PROCEDURE IF EXISTS prc_get_ambientes $$

CREATE PROCEDURE prc_get_ambientes()
COMMENT 'indistictly query all rows from ambiente tables'
BEGIN

	SELECT * FROM ambiente;


END $$

DELIMITER ;