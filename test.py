import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"

cursor.execute(create_table)

user = (1, 'jose', '123456')

insert_query = "INSERT INTO users VALUES (?,?,?)"

cursor.execute(insert_query, user)

users = [
    (2, 'rolf', '123456'),
    (3, 'anne', 'xyz')
]

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"

result = cursor.execute(select_query)

for row in result:
    print(row)

connection.commit()

connection.close()