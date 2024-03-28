import os
import sys

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.session import Session

app = Flask(__name__)
try:
    db_connection_uri = os.environ['DB_CONNECTION_URI']
    print('Successfully located environment variable, using value --', db_connection_uri, '--')
except KeyError as ke:
    print('Required database connection uri not found in environment variables:', ke)
    print('This should be something like -- mysql://uid:pwd@host:port/schema --')
    print('Continuing with default connection string -- mysql+pymysql://root:root@localhost:3306/northwind --')
    db_connection_uri = 'mysql+pymysql://root:root@localhost:3306/northwind'
print('Setting SQLALCHEMY_DATABASE_URI to --', db_connection_uri, '--')
app.config["SQLALCHEMY_DATABASE_URI"] = db_connection_uri

from entities.base import Base

db = SQLAlchemy(app, model_class=Base)

from entities.customer import Customer


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/all_customers')
def all_customers():
    with app.app_context():
        customer_list = db.session.query(Customer).all()
    return render_template('all_customers.html', customers=customer_list)


@app.route('/add_customer', methods=['POST'])
def add_customer_form():
    with app.app_context():
        session = Session(db)
        new_customer = Customer(name=request.form['customer_name'], contact_name=request.form['contact_name'],
                                address=request.form['address'], city=request.form['city'],
                                postal_code=request.form['postal_code'], country=request.form['country'])
        session.add(new_customer)
        session.commit()
    return render_template('customer_added.html', customer=new_customer)


@app.route('/delete_customer/<int:customer_id>')
def delete_customer(customer_id):
    with app.app_context():
        customer_to_delete = Customer.query.get(customer_id)
        db.session.delete(customer_to_delete)
        db.session.commit()
        customer_list = db.session.query(Customer).all()
    return render_template('all_customers.html', customers=customer_list)


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
