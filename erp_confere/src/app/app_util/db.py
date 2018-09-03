import MySQLdb


def get_db_resources():

	conn = MySQLdb.connect(host='192.168.33.50', port=3306,user='python'
		,password='Senh@1ndefinid4', db='erp',autocommit=False,charset='utf8mb4')

	cr = conn.cursor()

	return conn, cr

def query_with_one_result(sql_query, *args):

	conn, cur = get_db_resources()
	
	cur.execute(sql_query, args)
	returno = cur.fetchone()

	cur.close()
	conn.close()

	return returno

def execute_dml(sql_dml, *args):

	conn, cur = get_db_resources()
	
	cur.execute(sql_dml, args)
	conn.commit()	
	
	cur.close()
	conn.close()

	inserted_id = cur.lastrowid

	return inserted_id

