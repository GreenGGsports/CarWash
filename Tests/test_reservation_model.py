import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.reservation_model import ReservationModel  # Adjust import path as necessary
from datetime import datetime
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
def session(engine):
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_add_reservation(session):
    appointment = datetime.utcnow()
    reservation = ReservationModel.add_reservation(
        session=session,
        appointment_id=1,
        service_id=1,
        company_id=1,
        reservation_date=appointment,
        parking_spot='A1',
        car_type='Sedan',
        license_plate='ABC123',
        final_price=100.0
    )
    
    assert reservation.id is not None
    assert reservation.license_plate == 'ABC123'
    assert reservation.car_type == 'Sedan'

def test_read_reservation(session):
    reservation_date = datetime.utcnow()
    reservation = ReservationModel.add_reservation(
        session=session,
        appointment_id=1,
        service_id=1,
        company_id=1,
        reservation_date=reservation_date,
        parking_spot='B2',
        car_type='SUV',
        license_plate='DEF456',
        final_price=120.0
    )
    
    read_reservation = ReservationModel.get_by_id(session, reservation.id)
    assert read_reservation.id == reservation.id
    assert read_reservation.license_plate == 'DEF456'
    assert read_reservation.car_type == 'SUV'

def test_update_reservation(session):
    appointment = datetime.utcnow()
    reservation = ReservationModel.add_reservation(
        session=session,
        appointment_id=1,
        service_id=1,
        company_id=1,
        reservation_date=appointment,
        parking_spot='C3',
        car_type='Truck',
        license_plate='GHI789',
        final_price=150.0
    )
    
    updated_reservation = ReservationModel.update_by_id(
        session=session,
        obj_id=reservation.id,
        car_type='Van'
    )
    
    assert updated_reservation.car_type == 'Van'

def test_delete_reservation(session):
    appointment = datetime.utcnow()
    reservation = ReservationModel.add_reservation(
        session=session,
        appointment_id=1,
        service_id=1,
        company_id=1,
        reservation_date=appointment,
        parking_spot='D4',
        car_type='Coupe',
        license_plate='JKL012',
        final_price=180.0
    )
    
    result = ReservationModel.delete_by_id(session, reservation.id)
    assert result is True

    deleted_reservation = ReservationModel.get_by_id(session, reservation.id)
    assert deleted_reservation is None