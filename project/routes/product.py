import os
from datetime import datetime

from flask_login import login_required, current_user
from flask import render_template, Blueprint, flash, redirect, url_for, send_from_directory, request
from werkzeug.utils import secure_filename

from project import db
from project.forms.product import ProductForm
from project.models.order import BasketItem
from project.models.product import Product, ProductImage
from config import Config

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


@products_blueprint.route('/<product_id>/edit', methods=['GET', 'POST'])
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


@products_blueprint.route('/<product_id>', methods=['GET', 'POST'])
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


@products_blueprint.route('/images/<filename>')
def image(filename):
    return send_from_directory(Config.IMAGES_FOLDER, filename)


@products_blueprint.route('/<product_id>/images', methods=['GET'])
@login_required
def images(product_id):
    product = Product.query.filter_by(id=product_id).first_or_404()
    image_list = ProductImage.query.filter_by(product_id=product_id)
    return render_template('product_image_list.html', product=product, images=image_list,
                           title=f'{product} (Изображения)')


@products_blueprint.route('/<product_id>/images/upload', methods=['GET', 'POST'])
@login_required
def upload_image(product_id):
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    product = Product.query.filter_by(id=product_id).first_or_404()
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = f'{product_id}-{hash(file)}-{secure_filename(file.filename)}'
            file.save(os.path.join(Config.IMAGES_FOLDER, filename))
            p_image = ProductImage()
            p_image.product_id = product_id
            p_image.filename = filename
            db.session.add(p_image)
            db.session.commit()
            if product.primary_image_id is None:
                product.primary_image_id = p_image.id
                db.session.add(product)
                db.session.commit()
            return redirect(url_for('products.images', product_id=product_id))
    return render_template('product_image_upload.html', product=product, title=f'Добавить файл для {product}')
