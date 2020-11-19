from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    orders = db.relationship('Order', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Order {self.id}>'
