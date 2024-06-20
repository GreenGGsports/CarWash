import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.base import Base
from src.models.service_model import ServiceModel

@pytest.fixture(scope='module')
def engine():
    return create_engine('sqlite:///:memory:')

@pytest.fixture(scope='module')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def session(engine, tables):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create_service(session):
    service_name = "Test Service"
    price = 100
    service = ServiceModel.add_service(session, service_name, price)
    assert service.id is not None
    assert service.service_name == service_name
    assert service.price == price

def test_get_service(session):
    service_name = "Test Service"
    price = 100
    created_service = ServiceModel.add_service(session, service_name, price)
    fetched_service = ServiceModel.get_service(session, created_service.id)
    assert fetched_service is not None
    assert fetched_service.id == created_service.id
    assert fetched_service.service_name == service_name
    assert fetched_service.price == price

def test_get_services(session):
    service_name_1 = "Test Service 1"
    price_1 = 100
    service_name_2 = "Test Service 2"
    price_2 = 200
    ServiceModel.add_service(session, service_name_1, price_1)
    ServiceModel.add_service(session, service_name_2, price_2)
    services = ServiceModel.get_services(session)
    assert len(services) == 2
    assert services[0].service_name in [service_name_1, service_name_2]
    assert services[1].service_name in [service_name_1, service_name_2]

def test_update_service(session):
    service_name = "Test Service"
    price = 100
    new_service_name = "Updated Service"
    new_price = 150
    created_service = ServiceModel.add_service(session, service_name, price)
    updated_service = ServiceModel.update_service(session, created_service.id, service_name=new_service_name, price=new_price)
    assert updated_service.service_name == new_service_name
    assert updated_service.price == new_price

def test_delete_service(session):
    service_name = "Test Service"
    price = 100
    created_service = ServiceModel.add_service(session, service_name, price)
    ServiceModel.delete_service(session, created_service.id)
    deleted_service = ServiceModel.get_service(session, created_service.id)
    assert deleted_service is None
