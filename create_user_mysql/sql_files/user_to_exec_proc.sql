CREATE USER usr_create_user IDENTIFIED BY 'F0rr3stGump';

GRANT EXECUTE ON PROCEDURE mysql.prc_create_user TO 'usr_create_user';

FLUSH PRIVILEGES;
