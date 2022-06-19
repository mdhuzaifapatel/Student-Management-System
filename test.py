app.config['SECRET_KEY'] = "student"
# Database Creation
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
Migrate(app, db)

# Models
class Student(db.Model):
    __tableName__ = 'students'
    usn = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    
    def __repr__(self) -> str:
        return f"{self.usn} - {self.name}"