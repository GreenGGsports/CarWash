import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.slot_model import SlotModel
from setup import create_app
from src.models.base import BaseModel
from src.models.reservation_model import ReservationModel
from src.models.service_model import ServiceModel
from src.models.company_model import CompanyModel
from src.models.user_model import UserModel
from src.models.carwash_model import CarWashModel
from src.models.extra_model import ExtraModel
from src.models.reservation_extras import reservation_extra
from src.models.base import BaseModel
from src.models.carwash_model import CarWashModel

# Configure an in-memory SQLite database for testing
from src.models.reservation_extras import reservation_extra
from src.models.slot_model import SlotModel
from sessions import SessionFactory
from sqlalchemy import create_engine

@pytest.fixture(scope='module')
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
    

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client
            