import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.slot_model import SlotModel
from src.models.reservation_model import ReservationModel
from src.models.service_model import ServiceModel
from src.models.company_model import CompanyModel
from src.models.user_model import UserModel
from src.models.carwash_model import CarWashModel
from src.models.extra_model import ExtraModel
from src.models.reservation_extras import reservation_extra
from src.models.customer_model import CustomerModel
from src.models.base import BaseModel


# Configure an in-memory SQLite database for testing
@pytest.fixture(scope='function')
def engine():
    return create_engine('sqlite:///:memory:')

@pytest.fixture(scope='function')
def tables(engine):
    BaseModel.metadata.create_all(engine)
    yield
    BaseModel.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def session(engine, tables):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
