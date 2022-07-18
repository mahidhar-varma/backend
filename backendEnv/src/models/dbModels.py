from unicodedata import category
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
    documentFile = db.Column(db.LargeBinary, nullable=True)
