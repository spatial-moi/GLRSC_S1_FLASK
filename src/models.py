from sqlalchemy import inspect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy import Column, orm
from geoalchemy2 import Geometry

db = SQLAlchemy(engine_options={
    'max_overflow': 30,
    'pool_reset_on_return': 'commit',
    'pool_size': 20,
    'pool_timeout': 60
})
Base = orm.declarative_base()


class Account(db.Model, Base):
    # Auto Generated Fields:
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    created = db.Column(db.DateTime(timezone=True),
                        default=datetime.now)  # The Date of the Instance Creation => Created one Time when
    # Instantiation
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
    record_id = db.Column(db.Integer, primary_key=False, nullable=True, unique=True)

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


class MeetingRequest(db.Model, Base):
    # Auto Generated Fields:
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    created = db.Column(db.DateTime(timezone=True),
                        default=datetime.now)  # The Date of the Instance Creation => Created one Time when
    # Instantiation
    updated = db.Column(db.DateTime(timezone=True), default=datetime.now,
                        onupdate=datetime.now)  # The Date of the Instance Update => Changed with Every Update
    message = db.Column(db.String(75), nullable=False)
    buffer = Column(Geometry('POLYGON', srid=4326, spatial_index=True), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    account_id = db.Column(db.Integer, primary_key=False, nullable=True, unique=True)


class AccountRequest(db.Model, Base):
    account_id = db.Column(db.Integer, primary_key=True, nullable=True, unique=False)
    meeting_request_id = db.Column(db.Integer, primary_key=True, nullable=True, unique=False)


class ActiveMeeting(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    created = db.Column(db.DateTime(timezone=True),
                        default=datetime.now)  # The Date of the Instance Creation => Created one Time when Instantiation
    updated = db.Column(db.DateTime(timezone=True), default=datetime.now,
                        onupdate=datetime.now)  # The Date of the Instance Update => Changed with Every Update
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    account_id = db.Column(db.Integer, primary_key=False, nullable=True, unique=True)
    location = Column(Geometry('POINT', srid=4326, spatial_index=True), nullable=True)
    meeting_request_id = db.Column(db.Integer, primary_key=False, nullable=True, unique=False)
