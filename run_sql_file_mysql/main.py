import mysql.connector
import os


class MySQL_DB():

	default_database = 'mysql'

	def __init__(self, user, password, host, port):
		self.user = user
		self.password = password
		self.host = host
		self.port = port

	def get_connection(self):
		db_connection = mysql.connector.connect(user=self.user, password=self.password,
									host=self.host, port=self.port, database=self.default_database)

		return db_connection

	


def get_commands_from_file(filename):

	open_file = open(filename, 'r')
	file_content = open_file.read()
	file_commands = file_content.split(';')

	return [sql_command.replace(os.linesep, '') for sql_command in file_commands if sql_command != os.linesep] 

def get_command_from_file(filename):

	open_file = open(filename, 'r')
	file_content = open_file.read()

	return file_content


def close(resource):
	resource.close()


if __name__ == '__main__':

	sql_exec = get_commands_from_file('mudanca.sql')


	db = MySQL_DB('app_purge', 'Senh@1ndefinid4', '192.168.33.20', 3306)

	vagrant_db = db.get_connection()

	vagrant_cursor = vagrant_db.cursor()

	for sql in sql_exec: 
		print('Executando o comando {}'.format(sql))
		vagrant_cursor.execute(sql)


	close(vagrant_cursor)
	close(vagrant_db)




	

