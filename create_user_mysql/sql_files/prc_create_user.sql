DELIMITER $$

USE mysql $$

DROP PROCEDURE IF EXISTS prc_create_user $$

CREATE DEFINER='vyosiura' PROCEDURE prc_create_user(p_user VARCHAR(40), p_host VARCHAR(30),
								p_password VARCHAR(30), p_role ENUM('dev', 'qa', 'sup', 'app', 'dba'),
								p_env ENUM('prd', 'dev', 'qa'), p_execute TINYINT(1))
COMMENT 'Faz a criação do usuário de acordo com a sua função. parametros: \n\t "p_user" - usuário a ser criado: VARCHAR(40)\n\t "p_host" - host do usuário: VARCHAR(30)\n\t "p_password" - senha do novo usuário: VARCHAR(30)\n\t "p_role" - função do usuário: ENUM("dev", "qa", "sup", "app", "dba")\n\t "p_env" - ambiente que será criado: ENUM("prd", "dev", "qa")'
BEGIN

	-- DECLARE C_SQL_CREATE_USER VARCHAR(1000) DEFAULT "CREATE USER '#user'@'#host' IDENTIFIED BY '#password' WITH MAX_USER_CONNECTIONS 1";
	DECLARE C_SQL_CREATE_USER VARCHAR(1000) DEFAULT "CREATE USER '#user'@'#host' IDENTIFIED BY '#password'";
	DECLARE C_SQL_DROP_USER VARCHAR(1000) DEFAULT "DROP USER '#user'@'#host'";
	DECLARE C_SQL_PERMISSION_DATABASE_LEVEL_DML VARCHAR(1000) DEFAULT "GRANT INSERT, UPDATE, DELETE, SELECT, EXECUTE, SHOW VIEW ON #schema.* TO '#user'@'#host'";
	DECLARE C_SQL_PERMISSION_DATABASE_LEVEL_DQL VARCHAR(1000) DEFAULT "GRANT SELECT, SHOW VIEW ON #schema.* TO '#user'@'#host'";
	DECLARE C_SQL_PERSMISSION_OBJECT_TABLE_LEVEL_DML VARCHAR(1000) DEFAULT "GRANT INSERT, UPDATE, DELETE, SELECT, SHOW VIEW ON #schema.#table TO '#user'@'#host'";
	DECLARE C_SQL_PERMISSION_DATABASE_LEVEL_DDL_DML VARCHAR(1000) DEFAULT "GRANT INSERT, UPDATE, DELETE, SELECT, CREATE, ALTER, DROP, CREATE VIEW, LOCK TABLES, CREATE TEMPORARY TABLES, CREATE ROUTINE, ALTER ROUTINE, DROP ROUTINE, EXECUTE, REFERENCES, INDEX ON #schema.#table TO '#user'@'#host'";
	-- DBA
	DECLARE C_SQL_PERMISSION_GLOBAL_LEVEL_SUPER VARCHAR(1000) DEFAULT "GRANT ALL ON *.* TO '#user'@'#host' WITH GRANT OPTIONS";

	DECLARE v_user_exists INT;

	SET sql_log_bin = 0;
	-- Drop o usuário para recriar novamente com as devidas permissões --

	-- Drop all ocurrences of the current user----------------------------------------------------------------------
	BEGIN 
		DECLARE v_user_to_drop VARCHAR(30);
		DECLARE v_host_to_drop VARCHAR(30);
		DECLARE v_done_user_to_drop TINYINT(1) DEFAULT FALSE;
		DECLARE cr_user CURSOR FOR
		SELECT
			user,
			host
		FROM
			mysql.user 
		WHERE
			user = p_user;
		DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done_user_to_drop = TRUE;

		OPEN cr_user;

		loop_drop_user: LOOP 
			IF v_done_user_to_drop THEN
				LEAVE loop_drop_user;
			END IF;

			FETCH cr_user INTO v_user_to_drop, v_host_to_drop;

			IF v_user_to_drop = p_user THEN 
				SET @sql_drop_user = REPLACE(C_SQL_DROP_USER, '#user', v_user_to_drop);
				SET @sql_drop_user = REPLACE(@sql_drop_user, '#host', v_host_to_drop);

				IF p_execute = 1 THEN
					PREPARE stmt FROM @sql_drop_user;
					EXECUTE stmt;
					DEALLOCATE PREPARE stmt;
				ELSE 
					SELECT @sql_drop_user;
				END IF;
			END IF;
		END LOOP; 

		CLOSE cr_user;
	END ;

	SET @sql_create_user = REPLACE(REPLACE(REPLACE(C_SQL_CREATE_USER, '#user', p_user), '#host', p_host), '#password', p_password);

	IF p_execute THEN
		PREPARE stmt_create_user FROM @sql_create_user;
		EXECUTE stmt_create_user;
		DEALLOCATE PREPARE stmt_create_user;
	ELSE 
		SELECT @sql_create_user;
	END IF;

	IF p_env = 'prd' THEN
		-- Parte em que aplica as permissões.
		IF p_role IN('dev', 'qa', 'app') THEN
			-- Aplica permissão por database: %log, %data, %atende
			BEGIN
				DECLARE v_schema_name VARCHAR(40);
				DECLARE v_done TINYINT DEFAULT FALSE;
				DECLARE cr_schema_only CURSOR FOR
				SELECT
					schema_name
				FROM
					information_schema.schemata
				WHERE
					schema_name LIKE '%DATA'
				OR
					schema_name LIKE '%log______'
				OR
					schema_name LIKE '%log'
				OR
					schema_name LIKE '%atende'
				OR 
					schema_name LIKE 'etl_plataformas';

				DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = TRUE;

				OPEN cr_schema_only;
				lalp: LOOP

					FETCH cr_schema_only INTO v_schema_name;

					IF v_done THEN
						LEAVE lalp;
					END IF;

					IF p_role IN ('dev', 'qa') THEN
						SET @sql_grant_schema_priv = REPLACE(REPLACE(REPLACE(C_SQL_PERMISSION_DATABASE_LEVEL_DQL, '#user', p_user), '#host', p_host), '#schema', v_schema_name);
					ELSEIF p_role in ('app') THEN
						SET @sql_grant_schema_priv = REPLACE(REPLACE(REPLACE(C_SQL_PERMISSION_DATABASE_LEVEL_DML, '#user', p_user), '#host', p_host), '#schema', v_schema_name);
					END IF;

					IF p_execute THEN 
						PREPARE stmt_grant_priv FROM @sql_grant_schema_priv;
						EXECUTE stmt_grant_priv;
						DEALLOCATE PREPARE stmt_grant_priv;
					ELSE 
						SELECT @sql_grant_schema_priv;
					END IF;

				END LOOP;
				CLOSE cr_schema_only;
			END;

		ELSEIF p_role IN ('sup') THEN

			-- Por schema: data e log
			BEGIN
				DECLARE v_schema_name VARCHAR(50);
				DECLARE v_fim TINYINT(1) DEFAULT FALSE;

				DECLARE cr_schema CURSOR FOR
				SELECT
					schema_name
				FROM
					information_schema.schemata
				WHERE
					schema_name LIKE '%DATA'
				OR
					schema_name LIKE '%log______'
				OR
					schema_name LIKE '%log'
				OR 
					schema_name LIKE 'etl_plataformas';

				DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_fim = TRUE;

				OPEN cr_schema;

				sup_loop : LOOP
					FETCH cr_schema INTO v_schema_name;

					IF v_fim THEN
						LEAVE sup_loop;
					END IF;

					IF v_schema_name LIKE '%data' THEN
						SET @sql_grant_supp_priv = REPLACE(REPLACE(REPLACE(C_SQL_PERMISSION_DATABASE_LEVEL_DML, '#schema', v_schema_name), '#user', p_user), '#host', p_host);
					ELSE
						SET @sql_grant_supp_priv = REPLACE(REPLACE(REPLACE(C_SQL_PERMISSION_DATABASE_LEVEL_DQL, '#schema', v_schema_name), '#user', p_user), '#host', p_host);
					END IF;

					IF p_execute THEN 
						PREPARE stmt_grant_supp_priv FROM @sql_grant_supp_priv;
						EXECUTE stmt_grant_supp_priv;
						DEALLOCATE PREPARE stmt_grant_supp_priv;
					ELSE 
						SELECT @sql_grant_supp_priv;
					END IF;
				END LOOP;

				CLOSE cr_schema;
			END;

			-- Por tabela atende: DML
			BEGIN
				DECLARE v_schema_name VARCHAR(50);
				DECLARE v_table_name VARCHAR(50);
				DECLARE v_fim TINYINT(1) DEFAULT FALSE;

				DECLARE cr_schema_table CURSOR FOR
				SELECT
					table_schema,
					table_name
				FROM
					information_schema.tables
				WHERE
					table_schema LIKE '%atende'
				AND
					table_name IN ('configuracao', 'configuracao_condicao_ura', 'controle_configuracao', 'mensagem_ura', 'mensagem_web', 'grupo_funcionalidade',
						'mapa_navegacao_ura', 'mapa_navegacao_web', 'tipo_automacao_ura', 'transferencia_ura', 'configuracao_condicao_cliente', 'cliente_alto_valor',
					'tipo_atendimento_ura', 'chave_configuracao', 'cliente_aniblacklist', 'aeroportos');

				DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_fim = TRUE;

				OPEN cr_schema_table;

				loop_schema_table : LOOP

					FETCH cr_schema_table INTO v_schema_name, v_table_name;

					IF v_fim THEN
						LEAVE loop_schema_table;
					END IF;
					
					SET @sql_grant_supp_priv = REPLACE(REPLACE(REPLACE(REPLACE(C_SQL_PERSMISSION_OBJECT_TABLE_LEVEL_DML, '#schema', v_schema_name), '#user', p_user), '#host', p_host), '#table', v_table_name);

					IF p_execute THEN
						PREPARE stmt_grant_dml_priv FROM @sql_grant_supp_priv;
						EXECUTE stmt_grant_dml_priv;
						DEALLOCATE PREPARE stmt_grant_dml_priv;
					ELSE 
						 SELECT @sql_grant_supp_priv;
					END IF;

				END LOOP;

				CLOSE cr_schema_table;
			END;

			-- Por tabela atende: Consulta
			BEGIN

				DECLARE v_schema_name VARCHAR(50);
				DECLARE v_table_name VARCHAR(50);
				DECLARE v_fim TINYINT(1) DEFAULT FALSE;

				DECLARE cr_schema_table CURSOR FOR
				SELECT
					table_schema,
					table_name
				FROM
					information_schema.tables
				WHERE
					table_schema LIKE '%atende'
				AND
					table_name NOT IN ('configuracao', 'configuracao_condicao_ura', 'controle_configuracao', 'mensagem_ura', 'mensagem_web', 'grupo_funcionalidade',
						'mapa_navegacao_ura', 'mapa_navegacao_web', 'tipo_automacao_ura', 'transferencia_ura', 'configuracao_condicao_cliente', 'cliente_alto_valor',
					'tipo_atendimento_ura', 'chave_configuracao', 'cliente_aniblacklist', 'aeroportos');

				DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_fim = TRUE;

				OPEN cr_schema_table;
				loop_schema_table : LOOP

					FETCH cr_schema_table INTO v_schema_name, v_table_name;

					IF v_fim THEN
						LEAVE loop_schema_table;
					END IF;

					SET @sql_grant_supp_priv = REPLACE(REPLACE(REPLACE(REPLACE(C_SQL_PERMISSION_DATABASE_LEVEL_DQL, '#schema', v_schema_name), '#user', p_user), '#host', p_host), '#table', v_table_name);

					IF p_execute THEN 
						PREPARE stmt_grant_dml_priv FROM @sql_grant_supp_priv;
						EXECUTE stmt_grant_dml_priv;
						DEALLOCATE PREPARE stmt_grant_dml_priv;
					ELSE
						SELECT @sql_grant_supp_priv; 
					END IF;

				END LOOP;
			END;
	ELSEIF p_env = 'qa' THEN

		IF p_role IN ('qa', 'dev') THEN
			BEGIN 
				DECLARE v_schema_name VARCHAR(40);
				DECLARE v_done TINYINT(1) DEFAULT FALSE;
				DECLARE cr_cursor CURSOR FOR 
				SELECT
					v_schema_name
				FROM
					information_schema.tables
				WHERE	
					table_name NOT IN ('information_schema', 'performance_schema', 'mysql', 'sys');
				DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = TRUE;

				OPEN cr_cursor;

				qa_hom_loop : LOOP 

					IF v_done THEN
						LEAVE qa_hom_loop;
					END IF;

					FETCH cr_cursor INTO v_schema_name;	

					IF p_role = 'qa' THEN
						SET @sql_grant_privs_hom = REPLACE(REPLACE(REPLACE(C_SQL_PERMISSION_DATABASE_LEVEL_DML, '#user', p_user), '#host', p_host), '#schema', v_schema_name);
					ELSEIF p_role  ='dev' THEN
						SET @sql_grant_privs_hom = REPLACE(REPLACE(REPLACE(C_SQL_PERMISSION_DATABASE_LEVEL_DQL, '#user', p_user), '#host', p_host), '#schema', v_schema_name);
					END IF;	

					IF p_execute THEN
						PREPARE stmt_grant_priv_hom FROM @sql_grant_privs_hom;
						EXECUTE stmt_grant_priv_hom;
						DEALLOCATE PREPARE stmt_grant_priv_hom; 
					ELSE
						SELECT @sql_grant_privs_hom;
					END IF;

				END LOOP;

				CLOSE cr_cursor;
			END;
		END IF;
	ELSEIF p_env = 'dev' THEN
		BEGIN
			IF p_role IN ('qa', 'dev') THEN
				BEGIN 
					DECLARE v_schema_name VARCHAR(40);
					DECLARE v_done TINYINT(1) DEFAULT FALSE;
					DECLARE cr_cursor CURSOR FOR 
					SELECT
						v_schema_name
					FROM
						information_schema.tables
					WHERE	
						table_name NOT IN ('information_schema', 'performance_schema', 'mysql', 'sys');
					DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = TRUE;

					OPEN cr_cursor;

					qa_hom_loop : LOOP 

						IF v_done THEN
							LEAVE qa_hom_loop;
						END IF;

						FETCH cr_cursor INTO v_schema_name;	

						IF p_role = 'qa' THEN
							SET @sql_grant_privs_hom = REPLACE(REPLACE(REPLACE(C_SQL_PERMISSION_DATABASE_LEVEL_DQL, '#user', p_user), '#host', p_host), '#schema', v_schema_name);
						ELSEIF p_role  ='dev' THEN
							SET @sql_grant_privs_hom = REPLACE(REPLACE(REPLACE(C_SQL_PERMISSION_DATABASE_LEVEL_DDL_DML, '#user', p_user), '#host', p_host), '#schema', v_schema_name);
						END IF;	

						IF p_execute THEN
							PREPARE stmt_grant_priv_hom FROM @sql_grant_privs_hom;
							EXECUTE stmt_grant_priv_hom;
							DEALLOCATE PREPARE stmt_grant_priv_hom; 
						ELSE
							SELECT @sql_grant_privs_hom;
						END IF;
					END LOOP;

					CLOSE cr_cursor;
				END;
			END IF;			
		END;	
	ELSEIF p_role = 'dba' THEN

		SET @sql_grant_all = REPLACE(REPLACE(C_SQL_PERMISSION_GLOBAL_LEVEL_SUPER, '#user', p_user), '#host', p_host);

		IF p_execute THEN
			PREPARE stmt_dba FROM @sql_grant_all;
			EXECUTE stmt_dba;
			DEALLOCATE PREPARE stmt_dba;
		ELSE
			SELECT @sql_grant_all;
		END IF;
	END IF;

	FLUSH PRIVILEGES;
	FLUSH PRIVILEGES;

	SET sql_log_bin = 1;

END $$

DELIMITER ;