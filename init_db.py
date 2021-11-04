import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (TITLE) \
      VALUES ('You' )");
cur.execute("INSERT INTO posts (TITLE) \
      VALUES ('Avenegers' )");

# cur.execute("INSERT INTO posts (title)",


#             ('Second Post')
#             )

connection.commit()
connection.close()
