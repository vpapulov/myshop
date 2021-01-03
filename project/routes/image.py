import os
from flask_login import login_required
from flask import Blueprint, flash, redirect, url_for, request, send_from_directory
from werkzeug.utils import secure_filename

from config import Config

images_blueprint = Blueprint('images', __name__, url_prefix='/images', template_folder='templates')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@images_blueprint.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(Config.IMAGES_FOLDER, filename))
            return redirect(url_for('images.file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@images_blueprint.route('/<filename>')
def file(filename):
    return send_from_directory(Config.IMAGES_FOLDER, filename)
