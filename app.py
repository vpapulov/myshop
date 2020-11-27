from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config
from database import db
from routes import setup_routes

app = Flask(__name__)
app.config.from_object(Config)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
setup_routes(app)

if __name__ == '__main__':
    app.run()
