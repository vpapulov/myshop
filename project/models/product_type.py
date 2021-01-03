from project import db


class ProductType(db.Model):
    __tablename__ = 'product_type'
    ENTITY_NAME = 'Тип товара'
    ENTITY_NAME_PLURAL = 'Типы товара'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('product_type.id'), index=True)
    parent = db.relationship('ProductType')
    name = db.Column(db.String(150), index=True, nullable=False)

    def __repr__(self):
        return f'{ProductType.ENTITY_NAME} {self.name} ({self.id})'
