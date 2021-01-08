import os
from datetime import datetime

from flask_login import login_required
from flask import render_template, Blueprint, flash, redirect, url_for, send_from_directory, request
from werkzeug.utils import secure_filename

from project import db
from project.forms.product import ProductForm
from project.models.product import Product, ProductImage
from config import Config

products_blueprint = Blueprint('products', __name__, url_prefix='/products', template_folder='templates')


@products_blueprint.route('/')
@login_required
def product_list():
    item_list = Product.query.order_by('name').all()
    return render_template('product_list.html', title='Товары', item_list=item_list)


@products_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def product_new():
    product = Product()
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        form.populate_obj(product)
        db.session.add(product)
        db.session.commit()
        flash('Элемент успешно создан.')
        return redirect(url_for('products.product_list'))
    return render_template('product_edit.html', product=product, is_new=True, form=form)


@products_blueprint.route('/<product_id>/edit', methods=['GET', 'POST'])
@login_required
def product_edit(product_id):
    product = Product.query.filter_by(id=product_id).first_or_404()
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        form.populate_obj(product)
        db.session.add(product)
        db.session.commit()
        flash('Изменения были сохранены.')
        return redirect(url_for('products.product_list'))
    return render_template('product_edit.html', product=product, form=form)


@products_blueprint.route('/<product_id>', methods=['GET'])
@login_required
def product_view(product_id):
    obj = Product.query.filter_by(id=product_id).first_or_404()
    form = ProductForm(obj=obj)
    image_list = ProductImage.query.filter_by(product_id=product_id)
    primary_image = ProductImage.query.get(obj.primary_image_id)
    return render_template('product_view.html', title=obj, form=form, images=image_list, primary_image=primary_image)


@products_blueprint.route('/images/<filename>')
def image(filename):
    return send_from_directory(Config.IMAGES_FOLDER, filename)


@products_blueprint.route('/<product_id>/images', methods=['GET'])
@login_required
def images(product_id):
    product = Product.query.filter_by(id=product_id).first_or_404()
    image_list = ProductImage.query.filter_by(product_id=product_id)
    return render_template('product_images.html', product=product, images=image_list)


@products_blueprint.route('/<product_id>/images/upload', methods=['GET', 'POST'])
@login_required
def upload_image(product_id):
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = f'{product_id}-{hash(file)}-{secure_filename(file.filename)}'
            file.save(os.path.join(Config.IMAGES_FOLDER, filename))
            p_image = ProductImage()
            p_image.product_id = product_id
            p_image.filename = filename
            product = Product.query.filter_by(id=product_id).first_or_404()
            db.session.add(p_image)
            db.session.commit()
            if product.primary_image_id is None:
                product.primary_image_id = p_image.id
                db.session.add(product)
                db.session.commit()
            return redirect(url_for('products.images', product_id=product_id))
    return '''
    <!doctype html>
    <title>Добавление файла</title>
    <h1>Добавление файла</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Добавить>
    </form>
    '''
