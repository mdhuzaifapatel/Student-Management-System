# By Code Fellas
from __future__ import print_function
from mailmerge import MailMerge
from datetime import date
import win32api
import os
from flask import *
# from flaskwebgui import FlaskUI
from flask_sqlalchemy import SQLAlchemy
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = "fch345gvt36745bvb"
# ui = FlaskUI(app, maximized=True, close_server_on_exit=False)


############### Users Database ##############
conn = sqlite3.connect("signup.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Users(username TEXT, password TEXT)")
conn.commit()
conn.close()

############### Students Database ##############
conn = sqlite3.connect("students.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Students(usn TEXT, fullname TEXT, dob TEXT, branch TEXT, sem TEXT, placeofbirth TEXT, state TEXT, gender TEXT, address TEXT)")
conn.commit()
conn.close()


############### Routes ##############

############### Home Page ##############
@app.route('/')
def home():
    return render_template('home.html')

################## Signup Page ###################
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


################### Login Page ####################
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
                return redirect(url_for("dashboard"))
            else:
                msg = "Enter valid username and password"

    return render_template('login.html', msg=msg)


#################### Dashboard Page #####################
@app.route('/dashboard')
def dashboard():
    return render_template("index.html")

################### StudentRegister Page ##################
@app.route('/studentRegister', methods=['GET','POST'])
def studentRegister():
    if request.method == 'POST':
        usn = request.form['usn']
        fname = request.form['fname']
        dob = request.form['dob']
        branch = request.form['branch']
        sem = request.form['sem']
        pob = request.form['pob']
        state = request.form['state']
        gender = request.form['gender']
        address = request.form['address']

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Students (usn,fullname,dob,branch,sem,placeofbirth,state,gender,address) VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s")'%(usn,fname,dob,branch,sem,pob,state,gender,address))

        msg = 'Student registered sucessfully'
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    else:
        msg = 'Something went wrong'
    return render_template('student-details.html', msg=msg)


################### User Profile Page #####################
@app.route('/profile')
def profile():
    return render_template("users-profile.html")

################### Documents Page #####################
@app.route('/documents')
def documents():
    return render_template("documents.html")

################### Bonafide Page #####################
@app.route('/bonafide', methods=['GET','POST'])
def bonafide():
    
    msg = ""
    def details():
        r = ""
        if request.method == 'POST':
            usn = request.form['usn']
            conn = sqlite3.connect("students.db")
            c = conn.cursor()
            c.execute("SELECT * FROM Students WHERE usn ='" +
                  usn+"'")
            r = c.fetchall()
            # print(r)

            ################# Document Generator ######################
            d = r[0]
            usn = d[0]
            name = d[1].title()
            dob = d[2]
            branch = d[3]
            sem = d[4]

            # Define the templates - assumes they are in the same directory as the code
            bonafideTemplate = "Documents/bonafide.docx"
            bonafide = MailMerge(bonafideTemplate)

            # Info to be replaced
            bonafide.merge(
                name=name,
                branch=branch,
                usn=usn,
                sem=sem,
                # degree=degree,
                dob=dob,
                date='{:%d-%b-%Y}'.format(date.today()),
            )

            # Save the document
            bonafide.write(f'StudentDocs\{name}_Bonafide.docx')

            # Print the document
            filename = f'D:\Learning\PROJECTS\Mini Project\Student-Management-System\StudentDocs\{name}_Bonafide.docx'
            win32api.ShellExecute(0, 'print', filename, None, '.', 0)
                 
    details()
    return render_template("bonafide.html", msg=msg)
   

################# Logout session ####################


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


############### Main ##############
if __name__ == '__main__':
    # ui.run()
    app.run(debug=True, port=8000)
