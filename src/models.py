from sqlalchemy import inspect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy import Column, orm
from geoalchemy2 import Geometry

db = SQLAlchemy()
Base = orm.declarative_base()


# ----------------------------------------------- #

# SQL Datatype Objects => https://docs.sqlalchemy.org/en/14/core/types.html


class Account(db.Model, Base):
    # Auto Generated Fields:
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    created = db.Column(db.DateTime(timezone=True),
                         default=datetime.now)  # The Date of the Instance Creation => Created one Time when Instantiation
    updated = db.Column(db.DateTime(timezone=True), default=datetime.now,
                         onupdate=datetime.now)  # The Date of the Instance Update => Changed with Every Update

    # Input by User Fields:
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.LargeBinary, nullable=False)
    dob = db.Column(db.Date)
    city = db.Column(db.String(50))
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    sex = db.Column(db.String(50), nullable=True, unique=False)
    location = Column(Geometry('POINT', srid=4326, spatial_index=True), nullable=True)

    # Validations => https://flask-validator.readthedocs.io/en/latest/index.html

    # Set an empty string to null for username field => https://stackoverflow.com/a/57294872
    @validates('username')
    def empty_string_to_null(self, key, value):
        if isinstance(value, str) and value == '':
            return None
        else:
            return value

    # How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522
    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return "<%r>" % self.username
