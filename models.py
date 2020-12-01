from enum import Enum
from hashlib import md5

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from database import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    orders = db.relationship('Order', backref='user', lazy='dynamic')
    about_me = db.Column(db.String(500))
    last_seen = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Gender(Enum):
    Male = 1
    Female = 2


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_organization = db.Column(db.Boolean)
    organization_name = db.Column(db.String(200))
    gender = db.Column(db.Enum(Gender))
    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone_number = db.Column(db.String(100))
    address_line_1 = db.Column(db.String(100))
    address_line_2 = db.Column(db.String(100))
    address_line_3 = db.Column(db.String(100))
    town_city = db.Column(db.String(50))
    country = db.Column(db.String(50))


class ProductType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, index=True)
    name = db.Column(db.String(150), index=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True)
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_type.id'))
    description = db.Column(db.Text)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_order_placed = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    comment = db.Column(db.String(100))

    def __repr__(self):
        return f'<Order {self.id}>'


class OrderItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    quantity = db.Column(db.Numeric(precision=15, scale=3))
    price = db.Column(db.Numeric(precision=15, scale=2))
    amount = db.Column(db.Numeric(precision=15, scale=2))
