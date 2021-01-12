import os

from flask import Blueprint, send_from_directory, request, abort, \
    render_template, flash, redirect, url_for
from flask_login import login_required
from sqlalchemy import and_
from werkzeug.utils import secure_filename

from config import Config
from project import db
from project.models.image import ProductImage
from project.models.product import Product

images_blueprint = Blueprint('images', __name__, url_prefix='/images',
                             template_folder='templates')


@images_blueprint.route('/<int:image_id>')
def image(image_id):
    img = ProductImage.query.filter_by(id=image_id).first_or_404()
    return send_from_directory(Config.IMAGES_FOLDER, img.filename)


@images_blueprint.route('/product/<int:product_id>', methods=['GET'])
@login_required
def product_images(product_id):
    product = Product.query.filter_by(id=product_id).first_or_404()
    image_list = ProductImage.query.filter_by(product_id=product_id)
    return render_template('product_image_list.html', product=product,
                           images=image_list,
                           title=f'{product} (Изображения)')


@images_blueprint.route('/product/<int:product_id>/new',
                        methods=['GET', 'POST'])
@login_required
def image_new(product_id):
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
            img_name = f'{product_id}-{hash(file)}' \
                       f'-{secure_filename(file.filename)}'
            file.save(os.path.join(Config.IMAGES_FOLDER, img_name))
            p_image = ProductImage()
            p_image.product_id = product_id
            p_image.filename = img_name
            db.session.add(p_image)
            db.session.commit()
            if product.primary_image_id is None:
                product.primary_image_id = p_image.id
                db.session.add(product)
                db.session.commit()
            return redirect(
                url_for('images.product_images', product_id=product_id))
    return render_template('image_new.html', product=product,
                           title=f'Добавить файл для {product}')


@images_blueprint.route('/product/<int:product_id>/primary/resized/<int:size>',
                        methods=['GET'])
@login_required
def primary_image_resized(product_id, size):
    product = Product.query.filter_by(id=product_id).first_or_404()
    return resize_image(product.primary_image_id, size)


@images_blueprint.route(
    '/product/<int:product_id>/<int:image_id>/resized/<int:size>',
    methods=['GET'])
@login_required
def image_resized(product_id, image_id, size):
    img = ProductImage.query.filter(
        and_(ProductImage.id == image_id,
             ProductImage.product_id == product_id)).first_or_404()
    return resize_image(img.id, size)


def resize_image(image_id, size):
    allowed_sizes = [100, 250]
    if size not in allowed_sizes:
        abort(403)
    img = ProductImage.query.filter_by(id=image_id).first_or_404()
    original_path = os.path.join(Config.IMAGES_FOLDER, img.filename)
    dir_path = os.path.join(Config.IMAGES_FOLDER, str(size))
    if os.path.exists(os.path.join(dir_path, img.filename)):
        return send_from_directory(dir_path, img.filename)
    else:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        from PIL import Image
        with Image.open(original_path) as src_img:
            result_img = src_img.resize((size, size))
        result_img.save(os.path.join(dir_path, img.filename))
        return send_from_directory(dir_path, img.filename)
