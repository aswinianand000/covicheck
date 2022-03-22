from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150))
    p_id = db.Column(db.Integer)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    file_name = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    result = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    full_name = db.Column(db.String(150))
    facility_name = db.Column(db.String(150))
    contact = db.Column(db.String(15))
    patients = db.relationship('Patient')
