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
    print("here")
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute(
                "DELETE FROM posts WHERE title = '" + title + "'"
            )
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
        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute(
                "DELETE FROM posts WHERE title = '" + title + "'"
            )
            conn.execute(
                "INSERT INTO posts (TITLE, genre) VALUES (?, ?)",
                (title, content),
            )
            posts = conn.execute('SELECT * FROM posts ORDER BY TITLE').fetchall()
            conn.commit()
            conn.close()
            return render_template('index.html', posts=posts)
    return render_template('update.html')


@app.route('/recommend', methods=('GET', 'POST'))
def recommend():
    print("recommending")
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute(
                "DELETE FROM posts WHERE title = '" + title + "'"
            )
            conn.execute(
                "INSERT INTO posts (TITLE, genre) VALUES (?, ?)",
                (title, content),
            )
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('recommend.html')


if __name__ == "__main__":
    app.run()
