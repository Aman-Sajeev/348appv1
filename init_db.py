import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (TITLE,genre) \
      VALUES ('You', 'drama' )");
cur.execute("INSERT INTO posts (TITLE,genre,actor) \
      VALUES ('Avengers','Action', 'Robert Downey Jr' )");
cur.execute("INSERT INTO posts (TITLE,genre,actor) \
      VALUES ('How I Met Your Mother','Comedy', 'Neil Patrick Harris' )");
cur.execute("INSERT INTO posts (TITLE,genre,actor) \
      VALUES ('Breaking Bad','Drama', 'Brian Cranston' )");
cur.execute("INSERT INTO posts (TITLE,genre,actor) \
      VALUES ('Criminal Minds','Drama', 'Crazy guy' )");

# cur.execute("INSERT INTO posts (title)",


#             ('Second Post')
#             )

connection.commit()
connection.close()
