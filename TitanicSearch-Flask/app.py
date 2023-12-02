from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/besto/Desktop/Final/Titanic.sqlite'
db = SQLAlchemy(app)


class Passenger(db.Model):
    __tablename__ = 'Passengers'
    # Define your table columns here
    PassengerId = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    Age = db.Column(db.Integer)
    Sex = db.Column(db.String)
    Survived = db.Column(db.Integer)
    Embarked = db.Column(db.String)

    def __str__(self):
        return f"Passenger ID: {self.PassengerId}, Name: {self.Name}, Age: {self.Age}, Sex: {self.Sex}"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_age = request.form.get('age')
        search_gender = request.form.get('gender')

        if search_age:
            passengers = Passenger.query.filter_by(Age=int(search_age)).all()
        elif search_gender:
            passengers = Passenger.query.filter_by(Sex=search_gender).all()
        else:
            passengers = Passenger.query.all()
        return render_template('home.html', passengers=passengers)

    return render_template('home.html')


with app.app_context():
    app.run(debug=True)
