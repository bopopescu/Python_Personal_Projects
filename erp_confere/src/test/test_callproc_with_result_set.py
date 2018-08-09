import MySQLdb as db


try:
	con = db.connect(user='python',password='Senh@1ndefinid4',host='192.168.33.50',db='erp',port=3306)
	cr = con.cursor()
	cr.callproc('prc_get_cliente_by_id', (30,))
	row = cr.fetchone()
	print(row)
except:
	raise
finally:
	cr.close()
	con.close()