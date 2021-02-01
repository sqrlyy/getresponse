from app import db

class Segment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    segment = db.Column(db.String(255), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    tag = db.Column(db.String(255), nullable=False)
