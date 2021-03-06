from flask import Flask
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY TITLE').fetchall()
    # print(posts)
    conn.close()
    return render_template('index.html', posts=posts)


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    print(post)
    conn.close()
    if post is None:
        abort(404)
    return post


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        actor = request.form['actor']
        minutes = request.form['minutes']
        print(actor,minutes)
        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO posts (title, genre,actor,minutes) VALUES (?, ?, ?, ?) ",
                (title, content,actor,minutes),
            )
            conn.execute(
                "INSERT INTO TITLE (title) VALUES ( '" + str(title) + "')"
            )
            conn.execute(
                "INSERT INTO RUNTIME (minutes) VALUES ( '" + str(minutes) + "')"
            )
            conn.execute(
                "INSERT INTO CREW (Actor) VALUES ( '" + str(actor) + "')"
            )

            print('this is from title')
            print(conn.execute('SELECT * FROM TITLE'))
            print('this is from RUNTIME')
            print(conn.execute('SELECT * FROM RUNTIME'))
            print('this is from the actors one')
            print(str(conn.execute('SELECT * FROM CREW')))
            posts = conn.execute('SELECT * FROM posts ORDER BY TITLE').fetchall()
            conn.commit()
            conn.close()
            return render_template('index.html', posts=posts)

    return render_template('create.html')


@app.route('/remove', methods=('GET', 'POST'))
def remove():
    print("REMOVING")
    if request.method == 'POST':
        title = request.form['title']
        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute(
                "DELETE FROM posts WHERE title = '" + title + "'"
            )
            # id = conn.execute(
            #     "SELECT id FROM TITLE WHERE title = '" + title + "'"
            # ).fetchone()

            # conn.execute(
            #     "CREATE PROCEDURE Remover @tb nvarchar(30) AS DELETE * FROM  WHERE id =  " + id
            #     "GO; "
            # )

            # for i in ["TITLE",'MINUTES','CREW',"RATING"]:
            #     conn.execute(
            #         "EXEC Remover @tb = '" + i + "'"
            #     )
            posts = conn.execute('SELECT * FROM posts ORDER BY TITLE').fetchall()
            conn.commit()
            conn.close()
            return render_template('index.html', posts=posts)

    return render_template('remove.html')


@app.route('/update', methods=('GET', 'POST'))
def update():
    print("updating")
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        actor = request.form['actor']
        minutes = request.form['minutes']
        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            # updates the posts data with the new info
            conn.execute(
                "UPDATE posts SET genre = '" + content + "', " + "actor = '" + actor + "', "
                + "minutes = '" + minutes + "' WHERE title = '" + title + "'"
            )
            # conn.execute(
            #     "UPDATE  TITLE SET title =  '" + str(title) + "'"
            # )
            # conn.execute(
            #     "UPDATE  RUNTIME SET minutes =  " + str(minutes)
            # )
            # conn.execute(
            #     "UPDATE CREW SET Actor '" + str(actor) + "'"
            # )

            posts = conn.execute('SELECT * FROM posts ORDER BY TITLE').fetchall()
            conn.commit()
            conn.close()
            return render_template('index.html', posts=posts)
    return render_template('update.html')


@app.route('/recommend', methods=('GET', 'POST'))
def recommend():
    print("recommending")
    if request.method == 'POST':
        content = request.form['content']
        minutes = request.form['minutes']
        low = int(minutes) - 10
        high = int(minutes) + 10
        conn = get_db_connection()
        posts = conn.execute("SELECT * FROM posts WHERE genre = '" + content
                           + "' OR minutes BETWEEN " + str(low) + " AND " + str(high) + " ORDER BY TITLE").fetchall()

        conn.commit()
        conn.close()
        return render_template('index.html', posts=posts)

    return render_template('recommend.html')


if __name__ == "__main__":
    app.run()
