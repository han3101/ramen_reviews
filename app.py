import os, csv
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

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
    ramen_type = db.Column(db.String(100))
    package = db.Column(db.String(50), nullable=True)
    rating = db.Column(db.Float, nullable=True)

# db.create_all()

# with open('ramen-ratings.csv', 'r') as f:
#     csvreader = csv.reader(f)
#     counter = 0
#     next(csvreader)

#     for row in csvreader:
#         try:
#             review = Ramen(country=row[1], brand=row[2], ramen_type=row[3], package=row[4], rating=float(row[5]))
#         except ValueError:
#             review = Ramen(country=row[1], brand=row[2], ramen_type=row[3], package=row[4])
#         db.session.add(review)
#         db.session.commit()
        
#         counter += 1

#     print(counter)


# print(Ramen.query.get(5).ramen_type)
# print(Ramen.query.filter(Ramen.ramen_type == "").all())

@app.route('/')
def index():
    # Query the database and render the template
    countries = Ramen.query.with_entities(Ramen.country).distinct()
    reviews = Ramen.query.order_by(Ramen.rating.desc()).limit(5).all()
    return render_template('index.html', reviews=reviews, countries=countries)

@app.route('/update', methods=["POST", "PUT", "DELETE"])
# check for method
def router():
    method = request.method
    if method == "POST":
        add()
    elif method == "PUT":
        modify()
    elif method == "DELETE":
        delete()
    else:
        return url_for('index')

def add():
    # Get the form data and create a new record in the database
    country = request.form['country']
    brand = request.form['brand']
    type = request.form['type']
    package = request.form['package']
    rating = request.form['rating']
    new_review = Ramen(country=country, brand=brand, type=type, package=package, rating=rating)
    db.session.add(new_review)
    db.session.commit()
    return redirect(url_for('index'))

# def modify():
#     review_id = request.args.get('id')
#     review = Ramen.query.get(review_id)
#     return render_template('modify.html', review=review)

def modify():
    # Get the form data and update the corresponding record in the database
    review_id = request.form['id']
    review = Ramen.query.get(review_id)
    review.country = request.form['country']
    review.brand = request.form['brand']
    review.type = request.form['type']
    review.package = request.form['package']
    review.rating = request.form['rating']
    db.session.commit()
    return redirect(url_for('index'))

def delete():
    review_id = request.args.get('id')
    review = Ramen.query.get(review_id)
    try:
        db.session.delete(review)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "There was an issue deleting the review"

@app.route('/country', methods=["POST"])
def by_country():
    # Get the query parameter and filter the database by country
    country = request.form.get('country')
    country = country.strip("', /,, (, )")
    print(country)
    reviews = Ramen.query.filter_by(country=country).all()
    return render_template('search.html', reviews=reviews)

@app.route('/search', methods=["POST"])
def by_ptext():
    # Get the query parameter and filter the database by partial text match
    ptext = request.form.get('search')
    reviews = Ramen.query.filter(Ramen.ramen_type.contains(ptext)).all()
    return render_template('search.html', reviews=reviews)

