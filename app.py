# By Code Fellas
from forms import *
from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = "student"


############### Routes ############## 
@app.route('/')
def landingPage():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/loginValidate', methods=['POST'])
def loginValidate():
    username = request.form.get('username')
    password = request.form.get('password')
    return f"Username is {username} and Password is {password}"

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/dashboard')
def dashboard():
    return render_template("index.html")

@app.route('/studentRegister')
def studentRegister():
    return render_template("forms-elements.html")


############### Main ############## 
if __name__ == '__main__':
    app.run(debug=True, port=8000)
