from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from project.models.order import Customer


def customer_query():
    return Customer.query


class OrderForm(FlaskForm):
    date_order_placed = DateTimeField('Дата', validators=[DataRequired()], format='%d.%m.%Y %H:%M:%S',
                                      render_kw={'readonly': True, 'class': 'form-control'})
    customer = QuerySelectField('Покупатель', validators=[DataRequired()],
                                query_factory=customer_query,
                                get_label='name',
                                render_kw={'class': 'form-control'})
    comment = StringField('Комментарий', validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField('Сохранить',render_kw={'class': 'btn btn-info'})
