from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
