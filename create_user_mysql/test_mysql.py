import mysql.connector


def executesql(sql, conn):

	cr = conn.cursor()
	try:

		cr.execute(sql)
	except mysql.connector.ProgrammingError as e:
		print(e)
	else: 
		return cr


if __name__ == '__main__':

	con = mysql.connector.connect(user='app_purge', password='Senh@1ndefinid4', host='192.168.33.20', database='confere2')

	cr = executesql('create table te_py(a int)', con)

	for i in cr:
		print(i)

	con.close()