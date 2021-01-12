from project import db
from .customer import Customer
from .product import Product


class Order(db.Model):
    __tablename__ = 'order'
    ENTITY_NAME = 'Заказ'
    ENTITY_NAME_PLURAL = 'Заказы'
    id = db.Column(db.Integer, primary_key=True)
    date_order_placed = db.Column(db.DateTime, index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'),
                            nullable=False)
    customer = db.relationship(Customer)
    comment = db.Column(db.String(100))
    order_items = db.relationship("OrderItem")

    def __repr__(self):
        return f'Заказ {self.id} от ' \
               f'{self.date_order_placed.strftime("%d.%m.%Y")}'


class OrderItem(db.Model):
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), index=True,
                         nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
                           nullable=False)
    product = db.relationship(Product)
    quantity = db.Column(db.Numeric(precision=15, scale=3), nullable=False)
    price = db.Column(db.Numeric(precision=15, scale=2), nullable=False)
    amount = db.Column(db.Numeric(precision=15, scale=2), nullable=False)
