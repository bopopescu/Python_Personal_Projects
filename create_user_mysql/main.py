
# Create an app to execute a command in every database
import mysql.connector
import argparse
import string
import random
# ctrl + shit + p -> Anaconda: Disable linting on this file

DATABASE_CONFIG = {
	'vagrant': {
		'user': 'app_purge',
		'password': 'Senh@1ndefinid4',
		'host': '192.168.33.20',
		'port': 3306,
		'database': 'confere2'
	}
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
								port=db_info['port'], host=db_info['host'], database=db_info['database'])

	return con 


def executesql(sql, conn):

	cr = conn.cursor()

	cr.execute(sql)

	if cr.with_rows > 0:
		return cr 


def close(db_obj):
	db_obj.close()


if __name__ == '__main__':
	
	# All the option available through command line
	parser = argparse.ArgumentParser(description='Programa que cria todos os usuários nas bases dos bancos de dados da Mutant')
	parser.add_argument('-c', '--create', help='Operation to be created', action='store_true', required=True)
	parser.add_argument('user', help='Usuário a ser criado')

	arguments = parser.parse_args()

	if arguments.create:
		
		print(f'User to be created {arguments.user}')
		pswd = password_generator()

		for db in DATABASE_CONFIG.values():

			# Here execute the command
			tmp_con = conn_mysql(db)

			cur = executesql('select * from ambiente', tmp_con)
			# for value in cur:
			# 	print(value)

			print(cur.fetchall())

			close(cur)
			close(tmp_con)
			# executesql("call mysql.prc_create_user('{argument.user}')")
			
	else: 
		print('Marco idiota')




