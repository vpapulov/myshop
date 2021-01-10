from project import db
from project.models.product_type import ProductType


class Product(db.Model):
    __tablename__ = 'product'
    ENTITY_NAME = 'Товар'
    ENTITY_NAME_PLURAL = 'Товары'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True)
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_type.id'), nullable=False)
    product_type = db.relationship(ProductType)
    description = db.Column(db.Text)
    primary_image_id = db.Column(db.Integer, db.ForeignKey('product_image.id'))

    def __repr__(self):
        return f'"{self.name}" [код {self.id}]'


class ProductImage(db.Model):
    __tablename__ = 'product_image'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), index=True, nullable=False)
    filename = db.Column(db.String(255), nullable=False)
