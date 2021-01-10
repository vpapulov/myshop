from flask_login import login_required, current_user
from flask import render_template, Blueprint, flash, redirect, url_for

from project import db
from project.forms.product import ProductForm
from project.models.basket import BasketItem
from project.models.product import Product
from project.models.image import ProductImage

products_blueprint = Blueprint('products', __name__, url_prefix='/products', template_folder='templates')


@products_blueprint.route('/')
@login_required
def product_list():
    item_list = Product.query.order_by('name').all()
    return render_template('product_list.html', title=f'{Product.ENTITY_NAME_PLURAL}', item_list=item_list)


@products_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def product_new():
    product = Product()
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        form.populate_obj(product)
        db.session.add(product)
        db.session.commit()
        flash('Элемент успешно создан', 'success')
        return redirect(url_for('products.product_list'))
    return render_template('product_edit.html', product=product, is_new=True, form=form,
                           title=f'{product.ENTITY_NAME} (Новый)')


@products_blueprint.route('/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def product_edit(product_id):
    product = Product.query.filter_by(id=product_id).first_or_404()
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        form.populate_obj(product)
        db.session.add(product)
        db.session.commit()
        flash('Изменения были сохранены', 'success')
        return redirect(url_for('products.product_list'))
    return render_template('product_edit.html', product=product, form=form, title=f'{product}')


@products_blueprint.route('/<int:product_id>', methods=['GET', 'POST'])
@login_required
def product_view(product_id):
    product = Product.query.filter_by(id=product_id).first_or_404()
    form = ProductForm(obj=product)
    image_list = ProductImage.query.filter_by(product_id=product_id)
    primary_image = ProductImage.query.get(product.primary_image_id)
    if form.validate_on_submit():
        # add to basket
        basket_item = BasketItem()
        basket_item.user_id = current_user.id
        basket_item.product_id = product.id
        basket_item.quantity = form.quantity.data
        db.session.add(basket_item)
        db.session.commit()
        flash('Товар добавлен в корзину', 'info')
    return render_template('product_view.html', title=product, form=form, images=image_list,
                           primary_image=primary_image, product_id=product_id)
