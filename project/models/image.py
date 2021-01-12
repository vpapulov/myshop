from project import db


class ProductImage(db.Model):
    __tablename__ = 'product_image'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), index=True,
                           nullable=False)
    filename = db.Column(db.String(255), nullable=False)
