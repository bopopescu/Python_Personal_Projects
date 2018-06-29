#! /usr/bin/env python3
# Create an app to execute a command in every database
import mysql.connector
import argparse
import string
import random
import sys

import util.util as util
# ctrl + shit + p -> Anaconda: Disable linting on this file

DATABASE_CONFIG = {
	'spnetbd01': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.229.1.21', 'port': 3306, 'database': 'mysql'},
	'spnetbd02': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.229.1.22', 'port': 3306, 'database': 'mysql'},
	'recnetbd01': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.185.8.31', 'port': 3306, 'database': 'mysql'},
	'recnetbd02': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.185.8.32', 'port': 3306, 'database': 'mysql'},
	'poanetbd01': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.54.19.51', 'port': 3306, 'database': 'mysql'},
	'poanetbd02': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.54.19.52', 'port': 3306, 'database': 'mysql'},
	'brinetbd01': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.227.1.97', 'port': 3306, 'database': 'mysql'},
	'brinetbd02': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.227.1.98', 'port': 3306, 'database': 'mysql'},
	'spskybd01': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.228.1.120', 'port': 3306, 'database': 'mysql'},
	'spskybd02': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.228.1.121', 'port': 3306, 'database': 'mysql'},
	'bhznetbd01': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.0.132.61', 'port': 3306, 'database': 'mysql'},
	'bhznetbd02': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.0.132.62', 'port': 3306, 'database': 'mysql'},
	'rjoviabd01': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.230.50.72', 'port': 3306, 'database': 'mysql'},
	'rjoviabd02': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.230.50.73', 'port': 3306, 'database': 'mysql'},
	'bhznetaecbd01': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '192.168.226.248', 'port': 3306, 'database': 'mysql'},
	'bhznetaecbd02': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '192.168.226.222', 'port': 3306, 'database': 'mysql'},
	'frcmlzbd01': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.119.3.82', 'port': 3306, 'database': 'mysql'},
	'frcmlzbd02': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.119.3.83', 'port': 3306, 'database': 'mysql'},
	'bhzskybd01': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.228.2.90', 'port': 3306, 'database': 'mysql'},
	'bhzskybd02': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.228.2.91', 'port': 3306, 'database': 'mysql'},
	'ajunetbd01': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.229.3.18', 'port': 3306, 'database': 'mysql'},
	'ajunetbd02': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.229.3.19', 'port': 3306, 'database': 'mysql'},
	'fecnetbd01': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.226.1.100', 'port': 3306, 'database': 'mysql'},
	'fecnetbd02': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.226.1.101', 'port': 3306, 'database': 'mysql'},
	'spqlcbd01': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.230.1.104', 'port': 3306, 'database': 'mysql'},
	'spqlcbd03': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.230.1.106', 'port': 3306, 'database': 'mysql'},
	'rjonetbd01': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.229.4.102', 'port': 3306, 'database': 'mysql'},
	'rjonetbd02': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.229.4.104', 'port': 3306, 'database': 'mysql'},
	'jabnetbd01': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.229.6.131', 'port': 3306, 'database': 'mysql'},
	'jabnetbd02': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.229.6.161', 'port': 3306, 'database': 'mysql'},
	'spogolsbd01': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.119.5.113', 'port': 3306, 'database': 'mysql'},
	'spogolsbd02': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.119.5.114', 'port': 3306, 'database': 'mysql'},
	'spogolbd01': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.119.5.134', 'port': 3306, 'database': 'mysql'},
	'spogolbd02': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.119.5.135', 'port': 3306, 'database': 'mysql'},
	'olinetbd01': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.229.5.6', 'port': 3306, 'database': 'mysql'},
	'olinetbd02': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.229.5.53', 'port': 3306, 'database': 'mysql'},
	'spnetbdcent': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.229.1.135', 'port': 3306, 'database': 'mysql'},
	# 'spjgrbdcentral': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.81.1.56', 'port': 3306, 'database': 'mysql'},
	'spnetatebd': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.229.1.49', 'port': 3306, 'database': 'mysql'},
	'spnetbdna01': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.229.1.213', 'port': 3307, 'database': 'mysql'},
	'spvvjbd01': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '192.168.20.107', 'port': 3306, 'database': 'mysql'},
	'spvvjbd02': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '192.168.20.108', 'port': 3306, 'database': 'mysql'},
	'sppanbd01': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.119.6.58', 'port': 3306, 'database': 'mysql'},
	'sppanbd02': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.119.6.59', 'port': 3306, 'database': 'mysql'},
	'ossmdb': { 'user': 'usr_etl', 'password': 'lmsistemas01', 'host': '10.119.4.6', 'port': 3306, 'database': 'mysql'}
}

def password_generator(size=8, chars=string.ascii_letters + string.digits):
	"""
	Returns a string of random characters, useful in generating temporary
	passwords for automated password resets.

	size: default=8; override to provide smaller/larger passwords
	chars: default=A-Za-z0-9; override to provide more/less diversity

	Credit: Ignacio Vasquez-Abrams
	Source: http://stackoverflow.com/a/2257449
	"""
	return ''.join(random.choice(chars) for i in range(size))


def conn_mysql(db_info):

	con = mysql.connector.connect(user=db_info['user'], password=db_info['password'],
								port=db_info['port'], host=db_info['host'], database=db_info['database'],connection_timeout=30)

	return con


def executesql(sql, conn):

	cr = conn.cursor()
	cr.execute(sql)

	return cr

def mysql_execute_proc(conn, sql_str, *args):

	cnx = conn.cursor()
	stored_result = cnx.callproc('prc_create_user', args)
	close(cnx)

	return stored_result


def close(db_obj):
	db_obj.close()


def parseArguments():

	parser = argparse.ArgumentParser(description='Programa que cria todos os usuários nas bases dos bancos de dados URA da Mutant')

	parser.add_argument('-c', '--create', help='Operation to be created', action='store_true', required=True)
	parser.add_argument('user', help='Usuário a ser criado')
	parser.add_argument('role', help="Tipo de acesso do usuário: 'dev', 'sup', 'qa', 'app', 'dba'")

	return parser.parse_args()


if __name__ == '__main__':

	ROLES = ('dev', 'sup', 'qa', 'app', 'dba')
	# All the option available through command line
	arguments = parseArguments()

	if arguments.role not in ROLES:
		sys.exit("Role passada não informada. Possiveis roles: 'dev', 'sup', 'qa', 'app', 'dba'")

	if arguments.create:

		pswd = password_generator()
		print(f'Usuario a ser criado "{arguments.user}" com a senha "{pswd}"')

		for host, db in DATABASE_CONFIG.items():
			cur = None

			try:

				tmp_con = conn_mysql(db)

				executesql(util.SQL_DISABLE_LOG_BIN, tmp_con)

				is_log_bin_off = executesql(util.SQL_QUERY_LOG_BIN, tmp_con).fetchone()

				if is_log_bin_off[0] == 0 :
					mysql_execute_proc(tmp_con, util.SQL_PROC_CREATE_USER, arguments.user, '%', pswd, arguments.role, 'prd')
				else:
					print(f"sql_log_bin ativo no servidor: {host}")

			except Exception as err:

				exc_type, exc_obj, exc_tb = sys.exc_info()

				print(f'Linha {exc_tb.tb_lineno}: Erro no {host}: {str(err)}')

			else:

				print(f"{host}: Usuário criado com sucesso com sucesso: {arguments.user}")

			finally:

				try:
					close(tmp_con)
					close(is_log_bin_off)
					close(cur)

				except:
					pass

	else:
		sys.exit("Não foi passada a opção, favor informar a ação. Para mais informações utilize o '--help'")
