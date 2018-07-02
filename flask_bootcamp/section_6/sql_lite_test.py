import sqlite3

# Creates a file and stores the data in it
connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users(id int, username text, password text)"

cursor.execute(create_table)


user = (1,'jose','asdf')
insert_query="INSERT INTO users VALUES (?,?,?)"
cursor.execute(insert_query, user)


users = [
	(2, 'vini', 'asdf'),
	(3, 'anna', 'asdf')
]

cursor.executemany(insert_query,users)


select_query = "SELECT * FROM users"

rs = cursor.execute(select_query)

for row in rs:
	print(row)




connection.commit()

connection.close()