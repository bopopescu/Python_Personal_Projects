import ldap, sys 

from ldap3 import Server, Connection, ALL, NTLM


####################################################################################

con = ldap.initialize('ldap://10.221.1.30')

con.simple_bind_s('usr_bd@lmcorp.local', 'RD3Wd61@')

filter_condition = '(&(objectClass=person)(sAMAccountName=vyosiura))'
base_dn = 'dc=lmcorp,dc=local'



# [
# 	(
# 		'CN=Natalia Pereira Rocco,OU=Usuários_Grupos,OU=Testes,OU=Engenharia,OU=LMCORP,DC=lmcorp,DC=local', 
# 		 {
# 		 	'objectClass': [b'top', b'person', b'organizationalPerson', b'user'], 
# 		 	'cn': [b'Natalia Pereira Rocco'], 'sn': [b'Pereira Rocco'], 				
# 		 	'title': [b'ANALISTA DE TESTE JR'], 
# 		 	'description': [b'ANALISTA DE TESTE JR'], 
# 		 	'physicalDeliveryOfficeName': [b'PRIME SISTEMAS DE ATENDIMENTO AO CONSUMIDOR LTDA'], 
# 		 	'givenName': [b'Natalia'], 
# 		 	'distinguishedName': [b'CN=Natalia Pereira Rocco,OU=Usu\xc3\xa1rios_Grupos,OU=Testes,OU=Engenharia,OU=LMCORP,DC=lmcorp,DC=local'], 
# 		 	'instanceType': [b'4'], 
# 		 	'whenCreated': [b'20151221135302.0Z'], 
# 		 	'whenChanged': [b'20180801131430.0Z'], 
# 		 	'displayName': [b'NATALIA PEREIRA ROCCO'], 
# 		 	'uSNCreated': [b'15037679'], 
# 		 	'memberOf':[
# 		 			b'CN=GP_GL_ACESSO_BEARNED,OU=Usuarios_Grupos,OU=Bearned,DC=lmcorp,DC=local', 
# 		 			b'CN=GP_GL_Agentes_Jira,OU=Jira,DC=lmcorp,DC=local', 
# 		 			b'CN=GP_DL_ISE_WIRELESS,OU=ISE,OU=LMCORP,DC=lmcorp,DC=local', 
# 		 			b'CN=GP_GL_ISE_VPN,OU=Grupos,OU=Usuarios_Grupos,OU=Redes,OU=TI,OU=Operacional,OU=LMCORP,DC=lmcorp,DC=local', 
# 		 			b'CN=GP_DL_ISE_GLOBAL,OU=ISE,OU=LMCORP,DC=lmcorp,DC=local', 
# 		 			b'CN=GP_GL_TFS_TESTER,OU=Usu\xc3\xa1rios_Grupos,OU=Desenvolvimento,OU=Engenharia,OU=LMCORP,DC=lmcorp,DC=local', 
# 		 			b'CN=GP_GL_ProjectServer,CN=Builtin,DC=lmcorp,DC=local', 
# 		 			b'CN=GP_GL_Testes,OU=Usu\xc3\xa1rios_Grupos,OU=Testes,OU=Engenharia,OU=LMCORP,DC=lmcorp,DC=local', 
# 		 			b'CN=GP_GL_QA,OU=Usuarios_Grupos,OU=QA,OU=Financeiro e Processos,OU=LMCORP,DC=lmcorp,DC=local'], 
# 		 	'uSNChanged': [b'229313448'], 
# 		 	'department': [b'IVR'], 
# 		 	'company': [b'MUTANT'], 
# 		 	'name': [b'Natalia Pereira Rocco'], 
# 		 	'objectGUID': [b'\x1b\x18,\xdcp\x7f\xf9N\x87\x9e\xb7<\xc0\x86x\xa2'], 
# 		 	'userAccountControl': [b'514'], 
# 		 	'badPwdCount': [b'0'], 
# 		 	'codePage': [b'0'], 
# 		 	'countryCode': [b'0'], 
# 		 	'badPasswordTime': [b'131769386189520309'], 
# 		 	'lastLogoff': [b'0'], 
# 		 	'lastLogon': [b'131769386234050710'], 
# 		 	'pwdLastSet': [b'131738101703755110'], 
# 		 	'primaryGroupID': [b'513'], 
# 		 	'objectSid': [b'\x01\x05\x00\x00\x00\x00\x00\x05\x15\x00\x00\x00\xe7\xb1\xbcm\x99\xb5M` WePi3\x01\x00'], 
# 		 	'accountExpires': [b'9223372036854775807'], 
# 		 	'logonCount': [b'3781'], 
# 		 	'sAMAccountName': [b'natalia.rocco'], 
# 		 	'sAMAccountType': [b'805306368'], 
# 		 	'userPrincipalName': [b'natalia.rocco@lmcorp.local'], 
# 		 	'lockoutTime': [b'0'], 
# 		 	'objectCategory': [b'CN=Person,CN=Schema,CN=Configuration,DC=lmcorp,DC=local'], 
# 		 	'mSMQSignCertificates': [b'\x01\x00\x00\x00\xef\xd0\xb9\x03\xb4\x8c\xaf\x85`\x18Y?\xac\xf1\xe1\x1b\x818\xfd-\xbc0\x12N\xa0\xde\x11.\xc0=\x02)x\x03\x00\x000\x82\x03t0\x82\x02\\\xa0\x03\x02\x01\x02\x02\x04\xaa\xa5ZU0\r\x06\t*\x86H\x86\xf7\r\x01\x01\x05\x05\x000|1\x110\x0f\x06\x03U\x04\x07\x1e\x08\x00M\x00S\x00M\x00Q1\x0b0\t\x06\x03U\x04\n\x1e\x02\x00-1\x0b0\t\x06\x03U\x04\x0b\x1e\x02\x00-1M0K\x06\x03U\x04\x03\x1eD\x00L\x00M\x00C\x00O\x00R\x00P\x00\\\x00n\x00a\x00t\x00a\x00l\x00i\x00a\x00.\x00r\x00o\x00c\x00c\x00o\x00,\x00 \x00s\x00p\x00g\x00p\x00n\x00e\x00t\x00a\x00t\x00e\x00n\x00d0\x1e\x17\r160105113759Z\x17\r240105113759Z0|1\x110\x0f\x06\x03U\x04\x07\x1e\x08\x00M\x00S\x00M\x00Q1\x0b0\t\x06\x03U\x04\n\x1e\x02\x00-1\x0b0\t\x06\x03U\x04\x0b\x1e\x02\x00-1M0K\x06\x03U\x04\x03\x1eD\x00L\x00M\x00C\x00O\x00R\x00P\x00\\\x00n\x00a\x00t\x00a\x00l\x00i\x00a\x00.\x00r\x00o\x00c\x00c\x00o\x00,\x00 \x00s\x00p\x00g\x00p\x00n\x00e\x00t\x00a\x00t\x00e\x00n\x00d0\x82\x01"0\r\x06\t*\x86H\x86\xf7\r\x01\x01\x01\x05\x00\x03\x82\x01\x0f\x000\x82\x01\n\x02\x82\x01\x01\x00\x84\x8b\x84\xe4\xcc\x8c>\xc9o\xe8o\xec\xa5\x8a\xf2O\xc0P\x07S\r\x9f\xc2\x0eq\x10\x93\xc0\xdc\xb6\x03?c\x18\x8d\xaf\xa5.\xae\xedU\xf5\xb4\xee\xc5\xee\xafk\xb4\xa6\x02\xa9\xa22TlL|\xdaD\xa2!i1;\x9d\xd2\xfaZ5?\xf9w\xb1\xf0\xdaH\xc4Y\xc7\x04}\x8a\xc3\x14\xcbE\x1aA>\x13>\xf3w\x95\xc2\x8b\x85\x018\xca7\xaf\xd3 s\xf6\x1f1z/\x8f\x03\xf5\x97V\xa0\x85\x9fB\x91V\x98\x94\xa7\x03"Qc\x80\x18\x12!8/l\x86\x91B\\\x9d+"\xe1\x81@\x1b\xdd\x12c\x15\xbc\xffO\x82\xd9\x82\x80\xb1\xbe\x13\xf7w\x04\xb2n@rx8\x01\x8cW/\x9d\xa6D`\xb9\x80o\x9e\xb1\xb5c\xaa\xd0\xd6__\x109\x85\x87\xc9\x13\xcd$j\x8c\x1a\x7f\x8d\xb7\x02.P\x19\xdb\x88[\xcd\xa1}\xa3?\xb2E\xc0\xa9\xc27\xa66Z\x1f\xc3\xbcAP\x1d\xed\x86\xfd\xd5/\x1701\xee\x9d\x16?\xf9\xc3\xca\xbeE\xbe\x84\xb8\xba\x1a\xf2\xae\xa7\x02\x03\x01\x00\x010\r\x06\t*\x86H\x86\xf7\r\x01\x01\x04\x05\x00\x03\x82\x01\x01\x00Wat\xb5)\xd6\x10\xf1\xc7\xac\xe7\xde\x88D\xdf\xbc\n\x9cUkd\xd3\xad*\x10#z\xca\x05\xcf1\xb0&\xd9\x04^~\x00\xad\xe5\xc2\t\xb5K\xf6\\\xa6\xf7\xb6\xf8\x1b\x8by\x8a\x18\x95\xa8C\xee\x1c\x12\\\xea\xf9\xc9\xe3\xa4d\xdf\xb8(E?t\xbf\xc1\xaaZ|\x85\r\x1bk\x06\x19\xc2:\x83\xb4"\xdfvb\x89\xbd\x9bS\xef\xef\xc6\x08&\x81;\x0b\'\xe5\xbaE?0<\x05\x1ek\xdf\x91:K\xc5s\xb6Ln$+\xeeS\xed\xa4\xda8\xd8\x03O\xa9@\xa0Lq\xca\xccFlv\x06H\xb0\xd0\xa0\xf3X\xd37\xfe\x1c\x80o\xac\x8d\x9a\xd5\xed\xa6\xe1\xfe|\xc5\r6pM\xd9\x03\xa5T\xe0\x8aO\xdf\xd6\n\xaf.\xef3\xde\xa1H\xde\n\xa5,s\\\x8bE%\xae\x16\x86\x84\xcc \x89>\x1e\xbb\x1f\xc7K\xfb\xb5/\':\xdf\x04\xac\x94\xc0nF\x0f\xa0\x0e\x14!\x8f<}\xacQ\xd4\xc6\x07k\x14\xa6\xa1\xe9\xde\x1c8\xf3\xd3\x06\xe6\xacD]\xc0\x95W\xf0u'], 
# 		 	'mSMQDigests': [b'\xef\xd0\xb9\x03\xb4\x8c\xaf\x85`\x18Y?\xac\xf1\xe1\x1b'], 
# 		 	'dSCorePropagationData': [
# 		 		b'20180712161126.0Z', 
# 		 		b'20180710211236.0Z', 
# 		 		b'20180627160202.0Z', 
# 		 		b'20180529145513.0Z', 
# 		 		b'16010714223649.0Z'], 
# 		 	'lastLogonTimestamp': [b'131765655661596099'], 
# 		 	'mail': [b'natalia.rocco@mutantbr.com']
# 		 }
# 	)
# ]




####################################################################################

# usr_bd
# RD3Wd61@
DN, secret, un = sys.argv[1:4]

server = "ldap://10.22.1.31"
port = 389

base = "dc=LMCORP,dc=LOCAL"
scope = ldap.SCOPE_SUBTREE
filtering = "(&(objectClass=user)(sAMAccountName=" + un + "))"


attrs = ["*"]

l = ldap.initialize(server)
l.protocol_version = 3
l.set_option(ldap.OPT_REFERRALS, 0)

print(l.simple_bind_s(DN, secret))

r = l.search(base, scope, filtering, attrs)

typ, user = l.result(r,60)

name, attrs = user[0]

if hasattr(attrs, 'has_key') and attrs.has_key('displayName'):
	print(attrs)

sys.exit()
