import ldap


AD_SERVER = 'ldap://10.221.1.30'
AD_BASE_QUERY = '(&(objectClass=person)(saMAccountName={}))'
AD_USER = 'usr_bd@lmcorp.local'
AD_PASSWORD = 'RD3Wd61@'

BASE_DN = 'ou=LMCORP,dc=lmcorp,dc=local'

USER_DISABLED_ACCOUNT = 514
USER_NORMAL_ACCOUNT = 512
USER_ENABLED_PASSWORD_NEVER_EXPIRES = 66048


con = ldap.initialize(AD_SERVER)
con.simple_bind_s(AD_USER, AD_PASSWORD)
print(con.search_ext_s(BASE_DN, ldap.SCOPE_SUBTREE, AD_BASE_QUERY.format('dandrade')))




# Create a routine to create the user who exists in the AD 
# Create a routine to export a csv file with user who are disabled or 
