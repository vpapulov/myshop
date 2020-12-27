from enum import Enum

from project import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_order_placed = db.Column(db.DateTime, index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    customer = db.relationship("Customer")
    comment = db.Column(db.String(100))

    def __repr__(self):
        return f'<Order {self.id}>'


class OrderItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Numeric(precision=15, scale=3), nullable=False)
    price = db.Column(db.Numeric(precision=15, scale=2), nullable=False)
    amount = db.Column(db.Numeric(precision=15, scale=2), nullable=False)


class Gender(Enum):
    Male = 1
    Female = 2


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True, nullable=False)
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

    def __repr__(self):
        return f'{self.name}'


class ProductType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, index=True)
    name = db.Column(db.String(150), index=True, nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True)
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_type.id'), nullable=False)
    description = db.Column(db.Text)
