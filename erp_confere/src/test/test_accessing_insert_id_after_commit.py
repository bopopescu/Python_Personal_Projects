import MySQLdb as db 


conn = db.connect(host="192.168.33.50", port=3306, user="python", password="Senh@1ndefinid4", db="erp")

cur = conn.cursor()
saida = None
try:
	cur.callproc('prc_insert_funcao', (saida, 'MarcoIdiot'))
	cur.execute('SELECT @_prc_insert_funcao_0')
	saida = cur.fetchone()[0]
except:
	conn.rollback()
	raise
else:
	print('isso executa antes do commit')
	print('saida {}'.format(saida))		
finally:
	conn.commit()
	print('agora foi commitado')
	cur.close()
	conn.close()






