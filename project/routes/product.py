from flask_login import login_required
from flask import render_template, Blueprint, flash, redirect, url_for

from project import db
from project.forms.product import ProductForm
from project.models.product import Product

products_blueprint = Blueprint('products', __name__, url_prefix='/products', template_folder='templates')


@products_blueprint.route('/')
@login_required
def product_list():
    item_list = Product.query.order_by('name').all()
    return render_template('product_list.html', title='Товары', item_list=item_list)


@products_blueprint.route('/<int:entity_id>', methods=['GET', 'POST'])
@login_required
def product_view(entity_id):
    obj = Product.query.filter_by(id=entity_id).first_or_404()
    form = ProductForm(obj=obj)
    # if form.validate_on_submit():
    #     form.populate_obj(obj)
    #     db.session.add(obj)
    #     db.session.commit()
    #     flash('Изменения были сохранены.')
    #     return redirect(url_for('products.product_list'))
    return render_template('product_view.html', title=obj, form=form)


@products_blueprint.route('/edit/<int:entity_id>', methods=['GET', 'POST'])
@login_required
def product_edit(entity_id):
    obj = Product.query.filter_by(id=entity_id).first_or_404()
    form = ProductForm(obj=obj)
    if form.validate_on_submit():
        form.populate_obj(obj)
        db.session.add(obj)
        db.session.commit()
        flash('Изменения были сохранены.')
        return redirect(url_for('products.product_list'))
    return render_template('product_edit.html', title=obj, form=form)


@products_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def product_new():
    obj = Product()
    form = ProductForm(obj=obj)
    if form.validate_on_submit():
        form.populate_obj(obj)
        db.session.add(obj)
        db.session.commit()
        flash('Элемент успешно создан.')
        return redirect(url_for('products.product_list'))
    return render_template('product_edit.html', title=f'{Product.ENTITY_NAME} (Новый)', form=form)
