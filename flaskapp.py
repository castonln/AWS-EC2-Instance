from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from count_words_in_file import count_words_in_file

app = Flask(__name__)
app._static_folder = ''

DATABASE = 'var/www/html/flaskapp/users.db'
UPLOAD_ROOT = '/var/www/html/flaskapp/uploads'

# SQLite setup
conn = sqlite3.connect(DATABASE)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (username TEXT, password TEXT, firstname TEXT, lastname TEXT, email TEXT, address TEXT)''')
conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    address = request.form['address']

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, firstname, lastname, email, address) VALUES (?, ?, ?, ?, ?, ?)",
              (username, password, firstname, lastname, email, address))
    conn.commit()
    conn.close()

    return redirect(url_for('profile', username=username))

@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, password,))
    user = c.fetchone()

    if user is not None:
        return redirect(url_for('profile', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/profile/<username>')
def profile(username):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    
    user_uploads_filepath = os.path.join(UPLOAD_ROOT, username)
    wordcount = count_words_in_file(user_uploads_filepath)
    
    return render_template('profile.html', user=user, wordcount=wordcount)

@app.route('/profile/<username>', methods=['POST'])
def upload_file(username):
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        user_dir = os.path.join(UPLOAD_ROOT, username)
        # Create the directory if it doesn't exist
        os.makedirs(user_dir, exist_ok=True)
        save_path = os.path.join(user_dir, uploaded_file.filename)
        uploaded_file.save(save_path)
    return redirect(url_for('profile', username=username))

if __name__ == '__main__':
    app.run(debug=True)
