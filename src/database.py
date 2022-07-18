
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref



db = SQLAlchemy()



class User(db.Model):
    user_id = db.Column(db.String(6), primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email =  db.Column(db.String(30), unique=True, nullable=False)
    dob = db.Column(db.Date)
    mobile_no = db.Column(db.String(10), unique=True, nullable=False)
    gender = db.Column(db.String(1))
    user_login = db.relationship('User_Login', backref="user")
    # user_profile = db.relationship('User_Profile', backref="user")

class User_Login(db.Model):
    user_login_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(6), db.ForeignKey('user.user_id'), unique=True, nullable=False)
    # mobile_no = db.Column(db.String(10), db.ForeignKey('user.mobile_no'), unique=True, nullable=False)


# class User_Profile(db.Model):
#     user_profile_id = db.Column(db.String(6), primary_key=True)
#     user_id = db.Column(db.String(6), db.ForeignKey('user.user_id'))
    # profile_id = db.Column(db.String(6), db.ForeignKey('user.user_id'))

class documentModel(db.Model):
    __tablename__ = "documents"
    documentId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200), nullable=False)
    documentName = db.Column(db.String(200), nullable=False)
    doctorName = db.Column(db.String(200), nullable=False)
    hospitalName = db.Column(db.String(200), nullable=False)
    issuedDate = db.Column(db.String(200), nullable=False)
    documentURL = db.Column(db.String(200), nullable=False)
