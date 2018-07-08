import mysqlx 

erp_conn = {
	'host': '192.168.33.50',
	'port': 33060,
	'user': 'python',
	'password': 'Senh@1ndefinid4'
}

session = mysqlx.get_session(erp_conn)

erp = session.get_schema('erp')

tbl = erp.get_table('loja')

print(tbl.am_i_real())

loja = tbl.select()										\
		.where('cd_loja = :codigo OR nm_loja LIKE :loja')	\
		.bind('codigo', 2)									\
		.bind('loja', '%tode%')								\
		.execute()											\
		.fetch_all()

if loja: 
	print(loja[0]['cd_loja'])
	print(loja[1]['cd_loja'])



session.close()



