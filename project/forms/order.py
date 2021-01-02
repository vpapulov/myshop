from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from project.models.order import Customer


def customer_query():
    return Customer.query


class OrderForm(FlaskForm):
    date_order_placed = DateTimeField('Дата', validators=[DataRequired()], format='%d.%m.%Y %H:%M:%S')
    customer = QuerySelectField('Покупатель', validators=[DataRequired()],
                                query_factory=customer_query,
                                get_label='name')
    comment = StringField('Комментарий', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
