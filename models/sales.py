from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configs import Development
from datetime import datetime


app = Flask(__name__)
app.config.from_object(Development)

db = SQLAlchemy(app)


class SalesModel(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    inv_id = db.Column(db.Integer, db.ForeignKey('inventories.id'))
    qty = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
