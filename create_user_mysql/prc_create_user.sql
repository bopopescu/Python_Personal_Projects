DELIMITER $$

USE mysql $$

DROP PROCEDURE IF EXISTS prc_create_user $$

/*
	Proc para criação de usuários no banco

*/
CREATE DEFINER='vyosiura' PROCEDURE prc_create_user(p_user VARCHAR(40), p_host VARCHAR(30),
								p_password VARCHAR(30), p_role ENUM('dev', 'qa', 'sup', 'app', 'dba'),
								p_env ENUM('prd', 'dev', 'qa'))
COMMENT 'Faz a criação do usuário de acordo com a sua função. parametros: \n\t "p_user" - usuário a ser criado: VARCHAR(40)\n\t "p_host" - host do usuário: VARCHAR(30)\n\t "p_password" - senha do novo usuário: VARCHAR(30)\n\t "p_role" - função do usuário: ENUM("dev", "qa", "sup", "app", "dba")\n\t "p_env" - ambiente que será criado: ENUM("prd", "dev", "qa")'
BEGIN


	DECLARE v_create_user_dev_qa VARCHAR(1000) DEFAULT "CREATE USER '#user'@'#host' IDENTIFIED BY '#password' WITH MAX_USER_CONNECTIONS 1";
	DECLARE v_create_user_sup_app VARCHAR(1000) DEFAULT "CREATE USER '#user'@'#host' IDENTIFIED BY '#password'";

	--
	DECLARE v_permission_dev_qa_prod VARCHAR(1000) DEFAULT "GRANT SELECT, SHOW VIEW ON #schema.* TO '#user'@'#host'";

	-- Devido aos diferentes tipos de acesso o suporte necessita, foi necessário criar dessa forma
	DECLARE v_permission_sup_prod_schema_log VARCHAR(1000) DEFAULT v_permission_dev_qa_prod;
	DECLARE v_permission_sup_prod_schema_data VARCHAR(1000) DEFAULT "GRANT INSERT, UPDATE, DELETE, SELECT, EXECUTE, SHOW VIEW ON #schema.* TO '#user'@'#host'";
	DECLARE v_permission_sup_prod_table_atende_dml VARCHAR(1000) DEFAULT "GRANT INSERT, UPDATE, DELETE, SELECT, SHOW VIEW ON #schema.#table TO '#user'@'#host'";
	DECLARE v_permission_sup_prod_table_atende_dql VARCHAR(1000) DEFAULT "GRANT SELECT, SHOW VIEW ON #schema.#table TO '#user'@'#host'";

	-- App permissions
	DECLARE v_permission_app_prod VARCHAR(1000) DEFAULT "GRANT INSERT, UPDATE, DELETE, SELECT, SHOW VIEW, EXECUTE ON #schema.* TO '#user'@'#host'";

	-- DBA
	DECLARE v_permission_dba VARCHAR(1000) DEFAULT "GRANT ALL ON *.* TO '#user'@'#host' WITH GRANT OPTIONS";

	DECLARE v_user_exists INT;

	SET sql_log_bin = 0;
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
		-- SELECT @sql_drop_user;

	END IF;
	-- --------------------------------------------------------------------
	IF p_role IN ('dev', 'qa') THEN
		SET @sql_create_user = REPLACE(REPLACE(REPLACE(v_create_user_dev_qa, '#user', p_user), '#host', p_host), '#password', p_password);
	ELSEIF p_role IN ('sup', 'app', 'dba') THEN
		SET @sql_create_user = REPLACE(REPLACE(REPLACE(v_create_user_sup_app, '#user', p_user), '#host', p_host), '#password', p_password);
	END IF;
	PREPARE stmt_create_user FROM @sql_create_user;
	EXECUTE stmt_create_user;
	DEALLOCATE PREPARE stmt_create_user;
	-- SELECT @sql_create_user;

	-- Parte em que aplica as permissões.
	IF p_role in('dev', 'qa', 'app') THEN

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
					schema_name LIKE '%atende';
			DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = TRUE;

			OPEN cr_schema_only;
			lalp: LOOP

				FETCH cr_schema_only INTO v_schema_name;

				IF v_done THEN
					LEAVE lalp;
				END IF;

				IF p_role IN ('dev', 'qa') THEN
					SET @sql_grant_schema_priv = REPLACE(REPLACE(REPLACE(v_permission_dev_qa_prod, '#user', p_user), '#host', p_host), '#schema', v_schema_name);
				ELSEIF p_role in ('app') THEN
					SET @sql_grant_schema_priv = REPLACE(REPLACE(REPLACE(v_permission_app_prod, '#user', p_user), '#host', p_host), '#schema', v_schema_name);
				END IF;

				PREPARE stmt_grant_priv FROM @sql_grant_schema_priv;
				EXECUTE stmt_grant_priv;
				DEALLOCATE PREPARE stmt_grant_priv;

				-- SELECT @sql_grant_schema_priv;

			END LOOP;
			CLOSE cr_schema_only;

		END;

	ELSEIF p_role IN('sup') THEN

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
					schema_name LIKE '%log';

			DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_fim = TRUE;

			OPEN cr_schema;
			sup_loop : LOOP

				FETCH cr_schema INTO v_schema_name;

				IF v_fim THEN
					LEAVE sup_loop;
				END IF;

				IF v_schema_name LIKE '%data' THEN
					SET @sql_grant_supp_priv = REPLACE(REPLACE(REPLACE(v_permission_sup_prod_schema_data, '#schema', v_schema_name), '#user', p_user), '#host', p_host);
				ELSE
					SET @sql_grant_supp_priv = REPLACE(REPLACE(REPLACE(v_permission_sup_prod_schema_log, '#schema', v_schema_name), '#user', p_user), '#host', p_host);
				END IF;

				PREPARE stmt_grant_supp_priv FROM @sql_grant_supp_priv;
				EXECUTE stmt_grant_supp_priv;
				DEALLOCATE PREPARE stmt_grant_supp_priv;

				-- SELECT @sql_grant_supp_priv;

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

				SET @sql_grant_supp_priv = REPLACE(REPLACE(REPLACE(REPLACE(v_permission_sup_prod_table_atende_dml, '#schema', v_schema_name), '#user', p_user), '#host', p_host), '#table', v_table_name);

				PREPARE stmt_grant_dml_priv FROM @sql_grant_supp_priv;
				EXECUTE stmt_grant_dml_priv;
				DEALLOCATE PREPARE stmt_grant_dml_priv;

				-- SELECT @sql_grant_supp_priv;

			END LOOP;


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

				SET @sql_grant_supp_priv = REPLACE(REPLACE(REPLACE(REPLACE(v_permission_sup_prod_table_atende_dql, '#schema', v_schema_name), '#user', p_user), '#host', p_host), '#table', v_table_name);

				PREPARE stmt_grant_dml_priv FROM @sql_grant_supp_priv;
				EXECUTE stmt_grant_dml_priv;
				DEALLOCATE PREPARE stmt_grant_dml_priv;

				-- SELECT @sql_grant_supp_priv;

			END LOOP;
		END;

		-- Rotinas atende
	ELSEIF p_role IN ('dba') THEN

		SET @sql_grant_all = REPLACE(REPLACE(v_permission_dba, '#user', p_user), '#host', p_host);

		PREPARE stmt_dba FROM @sql_grant_all;
		EXECUTE stmt_dba;
		DEALLOCATE PREPARE stmt_dba;

		-- SELECT @sql_grant_all;

	END IF;

	FLUSH PRIVILEGES;
	FLUSH PRIVILEGES;

	SET sql_log_bin = 1;

END $$

DELIMITER ;
