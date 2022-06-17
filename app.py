# By Code Fellas

from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##############################################################
# DB Part - not complete yet
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    usn = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    branch = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return f"{self.usn}"
##############################################################

# Routes
@app.route('/')
def dashboard():
    return render_template("index.html");

@app.route('/login')
def login():
    return render_template("pages-login.html")

@app.route('/register')
def register():
    return render_template("pages-register.html")


if __name__ == '__main__':
    app.run(debug=True, port=8000)