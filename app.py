# By Code Fellas
from __future__ import print_function
from mailmerge import MailMerge
from datetime import date
import win32api
import os
from flask import *
# from flaskwebgui import FlaskUI
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = "fch345gvt36745bvb"
# ui = FlaskUI(app, maximized=True, close_server_on_exit=False)


############### Users Database ##############
conn = sqlite3.connect("signup.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Users(name TEXT, email TEXT, username TEXT, password TEXT, phone TEXT)")
conn.commit()
conn.close()

############### Students Database ##############
conn = sqlite3.connect("students.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Students(usn TEXT, fullname TEXT, fathername TEXT, dob TEXT, branch TEXT, sem TEXT, placeofbirth TEXT, state TEXT, gender TEXT, address TEXT)")
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
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            username = request.form['username']
            password = request.form['password']

            conn = sqlite3.connect("signup.db")
            c = conn.cursor()
            # c.execute("INSERT INTO Users VALUES('" +
                    #   username+"', '"+password+"')")
            c.execute('INSERT INTO Users (name,email,phone,username,password) VALUES("%s","%s","%s","%s","%s")'%(name,email,phone,username,password))
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

        # print(r)
        # print(userName)
        # print(password)

        if r == []:
            msg = "Incorrect username or password"

        else:
            
            for user in r:
                if userName == user[2] and password == user[3]:
                    session["loggedin"] = True
                    session["username"] = userName
                    session["name"] = user[0]
                    session["email"] = user[1]
                    session["phone"] = user[4]
                    return redirect(url_for("dashboard"))
                

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
        father = request.form['father']
        dob = request.form['dob']
        branch = request.form['branch']
        sem = request.form['sem']
        pob = request.form['pob']
        state = request.form['state']
        gender = request.form['gender']
        address = request.form['address']

        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Students (usn,fullname,fathername,dob,branch,sem,placeofbirth,state,gender,address) VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'%(usn,fname,father,dob,branch,sem,pob,state,gender,address))

        msg = 'Student registered sucessfully'
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    else:
        msg = 'Something went wrong'
    return render_template('student-details.html', msg=msg)

#################### Students Page #####################
@app.route('/students', methods=['GET','POST'])
def students():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("SELECT * FROM Students ")
    r = c.fetchall()
    # print(r)
    
    return render_template("students.html",student = r)

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
    def details():
        msg = ""
        r = ""
        if request.method == 'POST':
            usn = request.form['usn']
            conn = sqlite3.connect("students.db")
            c = conn.cursor()
            c.execute("SELECT * FROM Students WHERE usn ='" +
                  usn+"'")
            r = c.fetchall()
            print(r)
            if r == []:
                msg = "Student not found."
                return msg
            ################# Document Generator ######################
            else:
                d = r[0]
                usn = d[0]
                name = d[1].title()
                father = d[2].title()
                dob = d[3]
                branch = d[4]
                sem = d[5]

            
                bonafideTemplate = "Documents/bonafide.docx"
                bonafide = MailMerge(bonafideTemplate)

                # Info to be replaced
                bonafide.merge(
                    name=name,
                    father=father,
                    usn=usn,
                    sem=sem,
                    branch=branch,
                    dob=dob,
                    date='{:%d-%b-%Y}'.format(date.today()),
                )

                # Save the document
                bonafide.write(f'StudentDocs\Bonafide\{name}_Bonafide.docx')

                # Print the document
                filename = f'StudentDocs\Bonafide\{name}_Bonafide.docx'
                win32api.ShellExecute(0, 'print', filename, None, '.', 0)
                msg = "Bonafide generated sucessfully."
                return msg
                 
    d  = details()
    return render_template("bonafide.html", msg=d)

################### Study Certificate Page #####################
@app.route('/studyCertificate', methods=['GET','POST'])
def studyCertificate():
    def details():
        msg = ""
        r = ""
        if request.method == 'POST':
            usn = request.form['usn']
            conn = sqlite3.connect("students.db")
            c = conn.cursor()
            c.execute("SELECT * FROM Students WHERE usn ='" +
                  usn+"'")
            r = c.fetchall()
            # print(r)
            if r == []:
                msg = "Student not found."
                return msg
            ################# Document Generator ######################
            else:
                d = r[0]
                usn = d[0]
                name = d[1].title()
                father = d[2].title()
                dob = d[3]
                branch = d[4]
            
                studyCertificateTemplate = "Documents/studyCertificate.docx"
                studyCertificate = MailMerge(studyCertificateTemplate)

                # Info to be replaced
                studyCertificate.merge(
                    name=name,
                    father=father,
                    usn=usn,
                    branch=branch,
                    dob=dob,
                    date='{:%d-%b-%Y}'.format(date.today()),
                )

                # Save the document
                studyCertificate.write(f'StudentDocs\Study Certificate\{name}_StudyCertificate.docx')

                # Print the document
                filename = f'StudentDocs\Study Certificate\{name}_StudyCertificate.docx'
                win32api.ShellExecute(0, 'print', filename, None, '.', 0)
                msg = "Study Certificate generated sucessfully."
                return msg
                 
    d  = details()
    return render_template("study-certificate.html", msg=d)

################### About College Page #####################
@app.route('/aboutCollege')
def aboutCollege():
    return render_template("about-college.html")

################### App Info Page #####################
@app.route('/appInfo')
def appInfo():
    return render_template("app-info.html")

################# Logout session ####################
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

############### Main ##############
if __name__ == '__main__':
    # ui.run()
    app.run(debug=True, port=8000)