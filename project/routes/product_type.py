from flask_login import login_required
from flask import render_template, Blueprint, flash, redirect, url_for
from sqlalchemy import text

from project import db
from project.forms.product_type import ProductTypeForm
from project.models.product_type import ProductType

product_types_blueprint = Blueprint('product_types', __name__,
                                    url_prefix='/product_types',
                                    template_folder='templates')


@product_types_blueprint.route('/')
@login_required
def product_type_list():
    sql_text = text(
        'select '
        '   p.id, p.name, coalesce(pp.name, "") as parent_name '
        'from product_type as p '
        '   left join product_type as pp '
        '   on p.parent_id=pp.id '
        'order by p.name')
    item_list = db.session.query('id', 'name', 'parent_name').from_statement(
        sql_text).all()
    return render_template('product_type_list.html',
                           title=ProductType.ENTITY_NAME_PLURAL,
                           item_list=item_list)


@product_types_blueprint.route('/edit/<entity_id>', methods=['GET', 'POST'])
@login_required
def product_type_edit(entity_id):
    obj = ProductType.query.filter_by(id=entity_id).first_or_404()
    parent = ProductType.query.filter_by(id=obj.parent_id).first()
    form = ProductTypeForm(id=obj.id, name=obj.name, parent=parent)
    if form.validate_on_submit():
        obj.name = form.name.data
        if form.parent.data is not None:
            obj.parent_id = form.parent.data.id
        db.session.add(obj)
        db.session.commit()
        flash('Изменения были сохранены', 'success')
        return redirect(url_for('product_types.product_type_list'))
    return render_template('product_type_edit.html', title=obj, form=form)


@product_types_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def product_type_new():
    obj = ProductType()
    form = ProductTypeForm(obj=obj)
    if form.validate_on_submit():
        obj.name = form.name.data
        if form.parent.data is not None:
            obj.parent_id = form.parent.data.id
        db.session.add(obj)
        db.session.commit()
        flash(f'{ProductType.ENTITY_NAME} успешно создан', 'success')
        return redirect(url_for('product_types.product_type_list'))
    return render_template('product_type_edit.html',
                           title=f'{ProductType.ENTITY_NAME} (Новый)',
                           form=form)
