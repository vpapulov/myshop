from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms_sqlalchemy.orm import QuerySelectField
from wtforms.validators import DataRequired

from project.models.product_type import ProductType


class ProductTypeForm(FlaskForm):
    name = StringField('Наименование', validators=[DataRequired()],
                       render_kw={'class': 'form-control'})
    parent = QuerySelectField(
        'Родитель',
        validators=[],
        query_factory=lambda: ProductType.query,
        get_label='name',
        allow_blank=True,
        blank_text=f'Выберите {ProductType.ENTITY_NAME.lower()}...',
        render_kw={'class': 'form-control'})
    submit = SubmitField('Сохранить', render_kw={'class': 'btn btn-info'})
