from flask import Flask, render_template, flash, redirect, url_for
from config import Config
from forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User

@app.route('/')
def index():
    return render_template('index.html', title='Магазин')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Вход', form=form)


if __name__ == '__main__':
    app.run()
