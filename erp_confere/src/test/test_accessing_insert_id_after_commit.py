import MySQLdb as db 


conn = db.connect(host="192.168.33.50", port=3306, user="python", password="Senh@1ndefinid4", db="erp")

cur = conn.cursor()
saida = None
try:
	# cur.callproc('prc_get_pedido_servico_by_id', (1, 1))
	cur.execute('select @@character_set_client')
except:
	conn.rollback()
	raise
else:
	saida = cur.fetchone()
	print(saida)
finally:
	cur.close()
	conn.close()






