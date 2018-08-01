import MySQLdb as db 


conn = db.connect(host="192.168.33.50", port=3306, user="python", password="Senh@1ndefinid4", db="erp")

cur = conn.cursor()
saida = None
try:
	cur.callproc('prc_insert_funcao', ('MarcoIdiot', ))
except:
	conn.rollback()
	raise
else:
	saida = cur.lastrowid
finally:
	conn.commit()
	cur.close()
	conn.close()


print(saida)



