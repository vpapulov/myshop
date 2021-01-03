from enum import Enum
from project import db


class Gender(Enum):
    Male = 1
    Female = 2


class Customer(db.Model):
    __tablename__ = 'customer'
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
