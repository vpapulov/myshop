from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired


class NewOrderForm(FlaskForm):
    date_order_placed = DateTimeField('Дата', validators=[DataRequired()], format='%d.%m.%Y %H:%M:%S')
    customer = SelectField('Покупатель', validators=[DataRequired()], coerce=int)
    comment = StringField('Комментарий', validators=[DataRequired()])
    submit = SubmitField('Создать')


class OrderForm(FlaskForm):
    date_order_placed = DateTimeField('Дата', validators=[DataRequired()], format='%d.%m.%Y %H:%M:%S')
    customer = SelectField('Покупатель', validators=[DataRequired()], coerce=int)
    comment = StringField('Комментарий', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
