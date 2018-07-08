import MySQLdb


def get_connection():

	cnx = MySQLdb.connect(host='192.168.33.50', port=3306,user='python'
		,password='Senh@1ndefinid4', db='erp',autocommit=False)

	return cnx

def query_with_one_result(sql_query, *args):

	conn = get_connection()
	cur = conn.cursor()

	cur.execute(sql_query, args)
	returno = cur.fetchone()

	cur.close()
	conn.close()

	return returno

def execute_dml(sql_dml, *args):

	conn  = get_connection()
	cur = conn.cursor()

	cur.execute(sql_dml, args)
	conn.commit()

	cur.close()
	conn.close()
