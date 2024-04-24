from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   make_response)
from config import conn, cursor
import hashlib
import html

app = Flask(__name__)

@app.route('/')
def index():
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id int AUTO_INCREMENT, username varchar(32), password varchar(32), PRIMARY KEY(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS notes (id int AUTO_INCREMENT, username varchar(32), title varchar(50), text varchar(1000), PRIMARY KEY(id))")
    conn.commit()
    if request.cookies:
        login = request.cookies.get('username')
        action = '/profile'
        
        cursor.execute("SELECT id, title, text FROM notes WHERE username = %s ORDER BY id DESC", (login,))
        notes = cursor.fetchall()

        formatted_notes = []
        for id, title, text in notes:
            formatted_text = html.escape(text).replace('\n', '<br>')
            formatted_notes.append((str(id), title, formatted_text))

        return render_template('index.html', login=login, action=action, notes=formatted_notes)
    else:
        login = 'Вхід'
        action = '/login'
        return render_template('login.html')

@app.route('/new-note')
def title():
    return render_template('new-note.html')

@app.route('/note')
def note():
    id = request.args.get('id')
    login = request.cookies.get('username')

    cursor.execute("SELECT id, title, text FROM notes WHERE id = %s", (id))
    notes = cursor.fetchall()

    formatted_notes = []
    for id, title, text in notes:
        formatted_text = html.escape(text).replace('\n', '<br>')
        formatted_notes.append((str(id), title, formatted_text))

    return render_template('note.html', note=formatted_notes)

@app.route('/note-submit', methods=['POST'])
def submit():
    title = request.form['title']
    text = request.form['text']
    username = request.cookies.get('username')

    cursor.execute("INSERT INTO notes (username, title, text) VALUES (%s, %s, %s)", (username, title, text))
    conn.commit()
 
    return redirect(url_for('index'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/log', methods=['POST'])
def log():
    username = request.form['username']
    password = request.form['password']
    md5 = hashlib.md5(password.encode()).hexdigest()

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, md5))
    data = cursor.fetchall()

    if len(data) > 0:
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('username', username, max_age=2592000)
        return resp
    else:
        return render_template('login.html', error='login | password')

@app.route('/reg', methods=['POST'])
def reg():
    username = request.form['username']
    password = request.form['password']
    password2 = request.form['password']

    cursor.execute("SELECT username FROM users WHERE username = %s", (username))
    data = cursor.fetchall()

    if len(data) > 0:
        return render_template('register.html', error='exists')

    if len(username) == 0 or len(password) == 0 or len(password2) == 0:
        return render_template('register.html', error='=0')
    elif len(username) < 5 or len(username) > 20:
        return render_template('register.html', error='username')
    elif len(password) < 8 or len(password) > 20:
        return render_template('register.html', error='password')
    elif password != password2:
        return render_template('register.html', error='password != password2')
    else:
        md5 = hashlib.md5(password.encode()).hexdigest()

        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, md5))
        conn.commit()
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('username', username, max_age=2592000)
        return resp

@app.route('/profile')
def profile():
    login = request.cookies.get('username')
    return render_template('profile.html', username=login)

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('username')
    return response

@app.route('/update-note', methods=['POST'])
def update_note():
    title = request.form['title']
    text = request.form['text'].replace('<br>', '')
    id = request.args.get('id')

    cursor.execute("UPDATE notes SET title = %s, text = %s WHERE id = %s", (title, text, id))
    conn.commit()

    return redirect(url_for('index'))

@app.route('/delete-note')
def delete_note():
    id = request.args.get('id')

    cursor.execute("DELETE FROM notes WHERE id = %s", (id))
    conn.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host= '192.168.1.249')
