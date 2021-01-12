from project import db


class BasketItem(db.Model):
    __tablename__ = 'basket_item'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True,
                        nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
                           nullable=False)
    product = db.relationship('Product')
    quantity = db.Column(db.Numeric(precision=15, scale=3), nullable=False)
