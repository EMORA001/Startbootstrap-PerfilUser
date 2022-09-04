from flask_login import UserMixin
from . import db
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(35), unique=True)
    password = db.Column(db.String(30))
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    imagen = db.Column(db.LargeBinary)

class Comments(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(50))
    comentario = db.Column(db.String(250))

