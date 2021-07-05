from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'iuvbfuiohbvcuibsidhvb'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sadique5829!!'
app.config['MYSQL_DB'] = 'CODE'
mysql = MySQL(app)

@app.route('/')

@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account WHERE username = % s AND password = % s', (username, password, ))

        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = username
            session['email'] = account ['email']
            session['id'] = account['id']
            message = 'Logged in successfully!'
            return render_template('index.html', msg=message)
        else:
            message = 'Invalid username and password'
    return render_template('login.html', msg=message)

@app.route('/register', methods =['GET', 'POST'])
def register():
    message = ''
    #Checking entries
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        #Check if record is existing
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account WHERE username = % s', (username, ))
        account = cursor.fetchone()

        if account:
            message = 'This account already exists'
        elif not username or not password or not email:
            message = 'Please fill all fields'
        else:
            cursor.execute('INSERT INTO account VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            message = 'You have successfully registered !'
    elif request.method == 'POST':
        message = 'Please fill out the form.'
    return render_template('register.html', msg=message)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('login'))