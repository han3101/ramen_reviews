import csv
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ramen.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)

# db.drop_all()

class Ramen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(50), nullable=True)
    brand = db.Column(db.String(50), nullable=True)
    ramen_type = db.Column(db.String(100), nullable=True)
    package = db.Column(db.String(50), nullable=True)
    rating = db.Column(db.Float, nullable=True)

db.create_all()

with open('ramen-ratings.csv', 'r') as f:
    csvreader = csv.reader(f)
    counter = 0
    next(csvreader)

    for row in csvreader:
        try:
            review = Ramen(country=row[1], brand=row[2], ramen_type=row[3], package=row[4], rating=float(row[5]))
        except ValueError:
            review = Ramen(country=row[1], brand=row[2], ramen_type=row[3], package=row[4])
        db.session.add(review)
        db.session.commit()
        
        counter += 1

    print(counter)


print(Ramen.query.get(5).ramen_type)
print(Ramen.query.filter(Ramen.ramen_type == "").all())