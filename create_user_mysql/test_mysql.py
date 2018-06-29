import mysql.connector
import utility.util as util

def executesql(sql, conn):

	cr = conn.cursor()
	try:

		cr.execute(sql)
	except mysql.connector.ProgrammingError as e:
		print(e)
	else:
		return cr


if __name__ == '__main__':

		print(util.SQL_DISABLE_LOG_BIN)
	# con = mysql.connector.connect(user='usr_etl', password='lmsistemas01', host='10.221.1.43', database='netdata')
	# con.close()
    #
	# print(con.is_connected())
