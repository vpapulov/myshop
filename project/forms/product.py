from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from project.models.product_type import ProductType


class ProductForm(FlaskForm):
    name = StringField('Наименование', validators=[DataRequired()],
                       render_kw={'class': 'form-control'})
    product_type = QuerySelectField(
        'Тип товара', validators=[DataRequired()],
        query_factory=lambda: ProductType.query,
        get_label='name', render_kw={'class': 'form-control'}
    )
    description = TextAreaField(
        'Описание', validators=[],
        render_kw={'class': 'form-control', "rows": 11}
    )
    quantity = IntegerField(
        'Количество', validators=[],
        render_kw={'class': 'form-control',
                   'type': 'number', 'min': '1',
                   'value': '1',
                   'size': '3'}
    )
    submit = SubmitField('Сохранить', render_kw={'class': 'btn btn-info'})
