from flask import Flask
from flask_migrate import Migrate

from config import Config
from database import db, login_manager
from routes import init_routes
from errors import init_err_handlers

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db, transaction_per_migration=True)

init_err_handlers(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожайлуста войдите, чтобы получить доступ к этой странице.'

init_routes(app)

if __name__ == '__main__':
    app.run()
