# By Code Fellas
# from re import L
# from forms import *
from flask import *
from flaskwebgui import FlaskUI
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
import sqlite3
# import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "student"
# ui = FlaskUI(app, maximized=True, close_server_on_exit=False)


############### Users Database ##############
conn = sqlite3.connect("signup.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Users(username TEXT, password TEXT)")
conn.commit()
conn.close()


############### Routes ##############
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    r = ""
    msg = ""
    if request.method == 'POST':
        userName = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect("signup.db")
        c = conn.cursor()
        c.execute("SELECT * FROM Users WHERE username ='" +
                  userName+"' and password = '"+password+"'")
        r = c.fetchall()

        for user in r:
            if userName == user[0] and password == user[1]:
                session["loggedin"] = True
                session["username"] = userName
                return redirect(url_for("studentRegister"))
            else:
                msg = "Enter valid username and password"

    return render_template('login.html', msg=msg)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        if request.form['username'] != "" and request.form['password'] != "":
            username = request.form['username']
            password = request.form['password']

            conn = sqlite3.connect("signup.db")
            c = conn.cursor()
            c.execute("INSERT INTO Users VALUES('" +
                      username+"', '"+password+"')")
            msg = 'Account is created sucessfully'
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
    else:
        msg = 'Something went wrong'
    return render_template('signup.html', msg=msg)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    return render_template("index.html")


@app.route('/studentRegister')
def studentRegister():
    return render_template("forms-elements.html")

@app.route('/profile')
def profile():
    return render_template("users-profile.html")

############### Main ##############
if __name__ == '__main__':
    # ui.run()
    app.run(debug=True, port=8000)