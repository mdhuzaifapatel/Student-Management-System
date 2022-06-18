# By Code Fellas

from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Routes
@app.route('/')
def dashboard():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("pages-login.html")

@app.route('/register')
def register():
    return render_template("pages-register.html")

@app.route('/studentRegister')
def studentRegister():
    return render_template("forms-elements.html")


if __name__ == '__main__':
    app.run(debug=True, port=8000)