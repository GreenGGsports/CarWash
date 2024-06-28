import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from src.models.base import Base
from src.models.slot_model import SlotModel
from src.models.reservation_model import ReservationModel, CarTypeEnum
from src.controllers.booking_controller import get_slot_id

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

def test_is_slot_available(session):

    # Create a slot
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)
    slot = SlotModel.add_slot(session, start_time=start_time, end_time=end_time)

    # Ensure the slot is available before any reservation
    assert ReservationModel.is_slot_available(session, slot.id, start_time)

    # Create a reservation for the slot
    reservation = ReservationModel.add_reservation(
        session=session,
        slot_id=slot.id,
        service_id=1,
        company_id=1,
        user_id=1,
        reservation_date=start_time,
        parking_spot=1,
        car_type='small_car',
        final_price=100.0
    )

    # Ensure the slot is no longer available after the reservation
    assert not ReservationModel.is_slot_available(session, slot.id, start_time)

    # Check slot availability for a different day
    different_day = start_time + timedelta(days=1)
    assert ReservationModel.is_slot_available(session, slot.id, different_day)

    # Add another slot for the same day
    start_time_2 = start_time + timedelta(hours=1)
    end_time_2 = start_time_2 + timedelta(hours=1)
    slot_2 = SlotModel.add_slot(session, start_time=start_time_2, end_time=end_time_2)

    # Ensure the new slot is available
    assert ReservationModel.is_slot_available(session, slot_2.id, start_time_2)

    # Add a reservation for the new slot
    reservation_2 = ReservationModel.add_reservation(
        session=session,
        slot_id=slot_2.id,
        service_id=1,
        company_id=1,
        user_id=1,
        reservation_date=start_time_2,
        parking_spot=1,
        car_type='small_car',
        final_price=120.0
    )

    # Ensure the new slot is no longer available after the reservation
    assert not ReservationModel.is_slot_available(session, slot_2.id, start_time_2)

    # Ensure the original slot is still unavailable
    assert not ReservationModel.is_slot_available(session, slot.id, start_time)

def create_hourly_slots(session):
    start_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    end_time = start_time.replace(hour=17)
    current_time = start_time
    while current_time < end_time:
        slot_end_time = current_time + timedelta(hours=1)
        SlotModel.add_slot(session, start_time=current_time, end_time=slot_end_time)
        current_time = slot_end_time

def test_double_booking_only_available_or_earlier(session):
    # Létrehozzuk az óránkénti slotokat 8:00-tól 17:00-ig
    create_hourly_slots(session)

    # Foglalás 13:00-ra
    reservation_date_1 = datetime.now().replace(hour=13, minute=0, second=0, microsecond=0)
    slot_id_1 = get_slot_id(session, reservation_date_1)
    assert slot_id_1 is not None

    # Ellenőrizzük, hogy a visszaadott slot ID a 12:00-13:00-as időszakra vonatkozik-e
    reserved_slot_1 = SlotModel.get_by_id(session, slot_id_1)
    assert reserved_slot_1.start_time.hour == 12
    assert reserved_slot_1.end_time.hour == 13

    reservation_2 = ReservationModel.add_reservation(
        session=session,
        slot_id=slot_id_1,
        service_id=1,
        company_id=1,
        user_id=1,
        reservation_date= reservation_date_1,
        parking_spot=1,
        car_type='small_car',
        final_price=120.0
    )

    # Próbáljunk újra ugyanarra az időpontra foglalni
    slot_id_2 = get_slot_id(session, reservation_date_1)

    # Ellenőrizzük, hogy nem sikerült újra ugyanarra az időpontra foglalni
    assert slot_id_2 is not None
    assert slot_id_1 == slot_id_2 + 1 

    slot2 = SlotModel.get_by_id(session, slot_id_2)
    assert slot2.start_time.hour == 11
    assert slot2.end_time.hour == 12

    # Foglalás 12:00-ra (korábbi időpontra)
    reservation_date_3 = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
    slot_id_3 = get_slot_id(session, reservation_date_3)
    assert slot_id_3 is not None

    # Ellenőrizzük, hogy a visszaadott slot ID a 11:00-12:00-as időszakra vonatkozik-e
    reserved_slot_2 = SlotModel.get_by_id(session, slot_id_3)
    assert reserved_slot_2.start_time.hour == 11
    assert reserved_slot_2.end_time.hour == 12
