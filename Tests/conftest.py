import pytest
from setup import create_app
from src.models.base import BaseModel
from src.models.reservation_model import ReservationModel
from src.models.service_model import ServiceModel
from src.models.company_model import CompanyModel
from src.models.user_model import UserModel
from src.models.slot_model import SlotModel
from sessions import SessionFactory
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

@pytest.fixture(scope='function')
def app():
    app = create_app('testing')
    return app

@pytest.fixture(scope='function')
def engine():
    return create_engine('sqlite:///:memory:')

@pytest.fixture(scope='function')
def session(app, engine):
    BaseModel.metadata.create_all(engine)
    Session = SessionFactory(engine)
    session = Session.get_session()
    with app.app_context():
        yield session
    session.close()
    BaseModel.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client
