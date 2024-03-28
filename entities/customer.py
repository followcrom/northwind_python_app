from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import column_property

from northwind_web import db


class Customer(db.Model):
    __tablename__ = 'customers'

    id = column_property(Column('CustomerID', Integer, primary_key=True))
    name = column_property(Column('CustomerName', String))
    contact_name = column_property(Column('ContactName', String))
    address = column_property(Column('Address', String))
    city = column_property(Column('City', String))
    postal_code = column_property(Column('PostalCode', String))
    country = column_property(Column('Country', String))
