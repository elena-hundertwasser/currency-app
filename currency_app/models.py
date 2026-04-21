from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ExchangeRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    base = db.Column(db.String(10))
    currency = db.Column(db.String(10))
    rate = db.Column(db.Float)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
