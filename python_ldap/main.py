from ldap3 import Server, Connection, ALL, NTLM

# usr_bd
# RD3Wd61@

mutant = Server('10.221.1.30', get_info=ALL)

con = Connection(mutant,user='LMCORP\\usr_bd', password='RD3Wd61@', authentication=NTLM)

con.bind()

con.search('ou=Suporte,dc=LMCORP,dc=LOCAL', '(&(ou=Financeiro))')

print(con.entries)
