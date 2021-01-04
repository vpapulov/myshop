from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required

from config import Config
from project.errors import init_err_handlers

db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    initialize_extensions(app)
    register_blueprints(app)
    return app


def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, transaction_per_migration=True)
    init_err_handlers(app, db)

    # Flask-Login configuration
    login.init_app(app)
    login.login_view = 'users.login'
    login.login_message = 'Пожайлуста войдите, чтобы получить доступ к этой странице.'
    from project.models.user import User

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app):
    from project.routes.user import users_blueprint
    from project.routes.image import images_blueprint
    from project.routes.product import products_blueprint
    from project.routes.order import orders_blueprint
    from project.routes.product_type import product_types_blueprint

    app.register_blueprint(users_blueprint)
    app.register_blueprint(images_blueprint)
    app.register_blueprint(product_types_blueprint)
    app.register_blueprint(products_blueprint)
    app.register_blueprint(orders_blueprint)

    @app.route('/')
    @login_required
    def index():
        return render_template('index.html', title='Магазин')
