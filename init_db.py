import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (TITLE,genre) \
      VALUES ('You', 'drama' )");
cur.execute("INSERT INTO posts (TITLE,genre,actor) \
      VALUES ('Avenegers','Action', 'Robert Downey Jr' )");

# cur.execute("INSERT INTO posts (title)",


#             ('Second Post')
#             )

connection.commit()
connection.close()
