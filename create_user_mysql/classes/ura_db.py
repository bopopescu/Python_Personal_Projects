import mysql.connector

class UraDB():

    def __init__(self, user, password ,host ,port ,database):

        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.conn = mysql.connector.connect(user=self.user, password=self.password, host=self.host,
                            port=self.port, database=self.database)

    def is_open(self):

        return self.conn.is_connected()

    
