DELIMITER $$

USE mysql $$

DROP PROCEDURE IF EXISTS prc_create_user $$

/*
	Proc para criação de usuários no banco

*/
CREATE PROCEDURE prc_create_user(p_user VARCHAR(40), p_host VARCHAR(30), 
								p_password VARCHAR(30), p_role ENUM('dev', 'qa', 'sup', 'app'),
								p_env ENUM('prd', 'dev', 'qa'))
BEGIN
	
	 
	DECLARE v_create_user_dev_qa = 'CREATE USER #user@#host IDENTIFIED BY #password WITH MAX_USER_CONNECTIONS 1';
	DECLARE v_create_user_sup_app = 'CREATE USER #user@#host IDENTIFIED BY #password';

	DECLARE v_permission_dev_qa_prod VARCHAR(1000) = 'GRANT SELECT ON #schema.* TO #user@#host'; 
	

	DECLARE v_user_exists INT;


	/* Prod
		- dev -> permission by schema 
			SELECT EM TUDO COM NO MÁXIMO 1 USUÁRIO

		- qa -> permission by schema
			SELECT EM TUDO COM NO MÁXIMO 1 USUÁRIO
		
		- sup -> permission by tables and schema  
			schema %data -> INSERT, SELECT, UPDATE, DELETE 
			schema %log -> SELECT
			schema %atende -> algumas tabelas INSERT, UPDATE, DELETE
			outras só SELECT e executar algumas procs?
		

		- app -> permission by schema
			INSERT, UPDATE, DELETE, SELECT, EXECUTE  on all schemas 

	*/

	-- Drop o usuário para recriar novamente com as devidas permissões -- 
	SELECT
		1
	INTO
		v_user_exists
	FROM
		mysql.user
	WHERE
		user = p_user
	AND
		host = p_host;

	IF v_user_exists = 1 THEN

		SET @sql_drop_user = "DROP USER '#user'@'#host'";
		SET @sql_drop_user = REPLACE(@sql_drop_user, '#user', p_user);
		SET @sql_drop_user = REPLACE(@sql_drop_user, '#host', p_host);

		PREPARE stmt FROM @sql_drop_user;
		EXECUTE stmt;
		DEALLOCATE PREPARE stmt;

	END IF; 
	----------------------------------------------------------------------

	IF 
		BEGIN

		END ;



END $$


DELIMITER ;