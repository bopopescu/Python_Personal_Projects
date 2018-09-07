import MySQLdb as db
import contextlib 

try:
	previous_state = None
	con = db.connect(user='python',password='Senh@1ndefinid4',host='192.168.33.50',db='erp',port=3306)
	with contextlib.closing( con.cursor() ) as cr:
		cr = con.cursor()
		cr.callproc('prc_get_previous_status_pedido_servico', (1, 1, None))
		cr.execute('SELECT @_prc_get_previous_status_pedido_servico_2')
		previous_state = cr.fetchone()[0]
except:
	raise
finally:
	con.close()

is_changeable = previous_state == 'concluido' or previous_state == 'liberado' or not previous_state
print(is_changeable)
print(previous_state)