import os
import sys
import tempfile
import pytest

# Эта конструкция нужна, чтобы приложение было доступно из папки tests
sys.path.insert(1,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from project.models.user import User
from project import db


@pytest.fixture
def test_client():
    db_fd, db_fn = tempfile.mkstemp()
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_fn \
                                            + '?check_same_thread=False'
    app.config['TESTING'] = True
    app.config['BCRYPT_LOG_ROUNDS'] = 4  # Bcrypt algorithm hashing rounds
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF tokens in the Forms

    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)
        yield client

    os.close(db_fd)
    os.unlink(app.config['SQLALCHEMY_DATABASE_URI'])


@pytest.fixture(scope='module')
def init_database():

    db.create_all()

    user1 = User(username='test1', email='test1@gmail.com')
    db.session.add(user1)

    db.session.commit()

    yield db

    db.drop_all()


def test_home(test_client, init_database):
    r = test_client.get('/')
    assert r.status_code == 302
    user1 = User.query.first()
    assert user1.username == 'test`'
