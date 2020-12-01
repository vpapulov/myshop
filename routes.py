from datetime import datetime, timedelta
from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse

from forms import LoginForm, RegistrationForm, EditProfileForm, NewOrderForm
from models import User
from database import db


def init_routes(app):
    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            now = datetime.utcnow()
            if current_user.last_seen is None \
                    or now - current_user.last_seen > timedelta(minutes=1):  # to reduce writing into db
                db.session.add(current_user)
                current_user.last_seen = now
                db.session.commit()

    @app.route('/')
    @login_required
    def index():
        return render_template('index.html', title='Магазин')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Неверные имя пользователя или пароль')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        return render_template('login.html', title='Вход', form=form)

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Позравляем с регистрацией! Теперь вы можете войти')
            return redirect(url_for('login'))
        return render_template('register.html', title='Регистрация', form=form)

    @app.route('/user/<username>')
    @login_required
    def user(username):
        user = User.query.filter_by(username=username).first_or_404()
        posts = [
            {'author': user, 'body': 'Test post #1'},
            {'author': user, 'body': 'Test post #2'}
        ]
        return render_template('user.html', user=user, posts=posts)

    @app.route('/edit_profile', methods=['GET', 'POST'])
    @login_required
    def edit_profile():
        form = EditProfileForm(current_user.username)
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.about_me = form.about_me.data
            db.session.commit()
            flash('Изменения были сохранены.')
            return redirect(url_for('edit_profile'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.about_me.data = current_user.about_me
        return render_template('edit_profile.html', title='Изменить профиль',
                               form=form)

    @app.route('/order/new', methods=['GET', 'POST'])
    @login_required
    def new_order():
        form = NewOrderForm()
        return render_template('order_new.html', title='Новый заказ', form=form)
