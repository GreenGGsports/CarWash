import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from src.models.reservation_model import ReservationModel  # Adjust import path as necessary
from src.models.slot_model import SlotModel  # Adjust import path as necessary
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
        slot_id = 1,
        service_id = 1,
        company_id = 1,
        user_id = 1,
        reservation_date=appointment,
        parking_spot='A1',
        car_type='large_car',
        final_price=100.0
    )
    
    assert reservation.id is not None
    assert reservation.car_type == 'large_car'

def test_read_reservation(session):
    reservation_date = datetime.utcnow()
    reservation = ReservationModel.add_reservation(
        session=session,
        slot_id=1,
        service_id=1,
        company_id=1,
        user_id = 1,
        reservation_date=reservation_date,
        parking_spot='B2',
        car_type='large_car',
        final_price=120.0
    )
    
    read_reservation = ReservationModel.get_by_id(session, reservation.id)
    assert read_reservation.id == reservation.id
    assert read_reservation.car_type == 'large_car'

def test_update_reservation(session):
    appointment = datetime.utcnow()
    reservation = ReservationModel.add_reservation(
        session=session,
        slot_id=1,
        service_id=1,
        company_id=1,
        user_id = 1,
        reservation_date=appointment,
        parking_spot='C3',
        car_type='small_car',
        final_price=150.0
    )
    
    updated_reservation = ReservationModel.update_by_id(
        session=session,
        obj_id=reservation.id,
        car_type='large_car'
    )
    
    assert updated_reservation.car_type == 'large_car'

def test_delete_reservation(session):
    appointment = datetime.utcnow()
    reservation = ReservationModel.add_reservation(
        session=session,
        slot_id=1,
        service_id=1,
        company_id=1,
        user_id = 1,
        reservation_date=appointment,
        parking_spot='D4',
        car_type='large_car',
        final_price=180.0
    )
    
    result = ReservationModel.delete_by_id(session, reservation.id)
    assert result is True

    deleted_reservation = ReservationModel.get_by_id(session, reservation.id)
    assert deleted_reservation is None

def test_add_reservation_slot_unavailable(session):
    # Sample data
    company_id = 1
    service_id = 1
    slot_id = 1
    user_id = 1
    reservation_date = datetime.now() + timedelta(days=1)
    car_type = 'large_car'
    final_price = 100.0
    parking_spot = 1

    # Add an initial reservation
    ReservationModel.add_reservation(
        session=session,
        company_id=company_id,
        service_id=service_id,
        slot_id=slot_id,
        reservation_date=reservation_date,
        user_id=user_id,
        car_type=car_type,
        final_price=final_price,
        parking_spot=parking_spot
    )

    # Attempt to add a second reservation for the same slot and date
    with pytest.raises(Exception, match="Slot is not available for reservation"):
        ReservationModel.add_reservation(
            session=session,
            company_id=company_id,
            service_id=service_id,
            slot_id=slot_id,
            reservation_date=reservation_date,
            user_id=user_id,
            car_type=car_type,
            final_price=final_price,
            parking_spot=parking_spot
        )

        assert not ReservationModel.is_slot_available(session, slot_id, reservation_date)

def test_is_slot_available(session):
    # Sample data
    slot_id = 1
    reservation_date = datetime.now() + timedelta(days=1)

    # Ensure slot is available initially
    assert ReservationModel.is_slot_available(session, slot_id, reservation_date)

    # Add a reservation
    ReservationModel.add_reservation(
        session=session,
        company_id=1,
        service_id=1,
        slot_id=slot_id,
        reservation_date=reservation_date,
        user_id=1,
        car_type='large_car',
        final_price=100.0,
        parking_spot=1
    )

    # Ensure slot is not available after reservation
    assert not ReservationModel.is_slot_available(session, slot_id, reservation_date)
