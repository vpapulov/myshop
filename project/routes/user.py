from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime, timedelta

from project.forms.user import RegistrationForm, LoginForm, EditProfileForm
from project import db
from project.models.user import User

users_blueprint = Blueprint('users', __name__, url_prefix='/orders',
                            template_folder='templates')


@users_blueprint.before_request
def before_request():
    if current_user.is_authenticated:
        now = datetime.utcnow()
        if current_user.last_seen is None or (
                now - current_user.last_seen > timedelta(
                minutes=1)):  # to reduce writing to database
            db.session.add(current_user)
        current_user.last_seen = now
        db.session.commit()


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        usr = User.query.filter_by(username=form.username.data).first()
        if usr is None or not usr.check_password(form.password.data):
            flash('Неверные имя пользователя или пароль', 'error')
            return redirect(url_for('users.login'))
        login_user(usr, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Вход', form=form)


@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        usr = User(username=form.username.data, email=form.email.data)
        usr.set_password(form.password.data)
        db.session.add(usr)
        db.session.commit()
        flash('Позравляем с регистрацией! Теперь вы можете войти', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Регистрация', form=form)


@users_blueprint.route('/<username>')
@login_required
def user(username):
    usr = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=usr, title=f'{usr}')


@users_blueprint.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Изменения были сохранены', 'success')
        return redirect(url_for('users.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Изменить профиль',
                           form=form)
