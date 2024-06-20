import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.models.reservation_model import ReservationModel  # Adjust the import according to your project structure
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base  # noqa: F811
import datetime
from src.models.company_model import CompanyModel as Company
from src.models.service_model import ServiceModel as Service
# Creating a new Base for the test environment
from src.models.base import Base


# Configure an in-memory SQLite database for testing
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

def test_add_reservation(session):
    # Adding a company and service to satisfy foreign key constraints

    appointment = datetime.datetime.utcnow()
    reservation = ReservationModel.add_reservation(
        session=session,
        appointment=appointment,
        license_plate='ABC123',
        name='John Doe',
        phone_number='1234567890',
        brand='Toyota',
        type='Sedan',
        company_id=1,
        service_id=1,
        parking_spot='A1'
    )
    
    assert reservation.id is not None
    assert reservation.name == 'John Doe'
    assert reservation.license_plate == 'ABC123'

def test_read_reservation(session):
    
    appointment = datetime.datetime.utcnow()
    reservation = ReservationModel.add_reservation(
        session=session,
        appointment=appointment,
        license_plate='DEF456',
        name='Jane Doe',
        phone_number='0987654321',
        brand='Honda',
        type='SUV',
        company_id=1,
        service_id=1,
        parking_spot='B2'
    )
    
    read_reservation = ReservationModel.read_reservation(session, reservation.id)
    assert read_reservation.id == reservation.id
    assert read_reservation.name == 'Jane Doe'

def test_update_reservation(session):
    appointment = datetime.datetime.utcnow()
    reservation = ReservationModel.add_reservation(
        session=session,
        appointment=appointment,
        license_plate='GHI789',
        name='Jim Doe',
        phone_number='1112223333',
        brand='Ford',
        type='Truck',
        company_id=1,
        service_id=1,
        parking_spot='C3'
    )
    
    updated_reservation = ReservationModel.update_reservation(
        session=session,
        reservation_id=reservation.id,
        name='Jimmy Doe'
    )
    
    assert updated_reservation.name == 'Jimmy Doe'

def test_delete_reservation(session):    
    appointment = datetime.datetime.utcnow()
    reservation = ReservationModel.add_reservation(
        session=session,
        appointment=appointment,
        license_plate='JKL012',
        name='Jake Doe',
        phone_number='4445556666',
        brand='Chevrolet',
        type='Coupe',
        company_id=1,
        service_id=1,
        parking_spot='D4'
    )
    
    result = ReservationModel.delete_reservation(session, reservation.id)
    assert result is True

    deleted_reservation = ReservationModel.read_reservation(session, reservation.id)
    assert deleted_reservation is None
