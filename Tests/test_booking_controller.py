from datetime import datetime, timedelta
from src.models.slot_model import SlotModel
from src.models.reservation_model import ReservationModel
from src.controllers.booking_controller import get_slot_id, get_earliest_available_slot
import pytest
from src.models.car_model import CarModel
from sqlalchemy.orm import Session

@pytest.fixture
def setup_database(session: Session):
    # Clean up the database before the test starts
    session.query(ReservationModel).delete()
    session.commit()

    car1 = CarModel(license_plate='xyz-123', car_type = 'small_car', car_brand = 'Bugatti')
    session.add(car1)
    session.commit()

    yield

def test_is_slot_available(session, setup_database):

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
        customer_id=1,
        carwash_id=1,
        reservation_date=start_time,
        parking_spot=1,
        car_id =  1
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
        customer_id=1,
        carwash_id=1,
        reservation_date=start_time_2,
        parking_spot=1,
        car_id =  1
    )

    # Ensure the new slot is no longer available after the reservation
    assert not ReservationModel.is_slot_available(session, slot_2.id, start_time_2)

    # Ensure the original slot is still unavailable
    assert not ReservationModel.is_slot_available(session, slot.id, start_time)

def create_hourly_slots(session):
    start_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    end_time = start_time.replace(hour=17)
    SlotModel.create_default_slots(session = session, start_time=start_time,end_time=end_time, slot_duration_minutes=60)

def test_double_booking_only_available_or_earlier(session, setup_database):
    # Create hourly slots from 8:00 to 17:00
    create_hourly_slots(session)

    # Booking for 13:00
    reservation_date_1 = datetime.now().replace(hour=13, minute=0, second=0, microsecond=0)
    slot_id_1 = get_slot_id(session, reservation_date_1)
    assert slot_id_1 is not None

    # Check if the returned slot ID corresponds to the 12:00-13:00 period
    reserved_slot_1 = SlotModel.get_by_id(session, slot_id_1)
    assert reserved_slot_1.start_time.hour == 12
    assert reserved_slot_1.end_time.hour == 13

    reservation_2 = ReservationModel.add_reservation(
        session=session,
        slot_id=slot_id_1,
        service_id=1,
        customer_id=1,
        carwash_id=1,
        reservation_date=reservation_date_1,
        parking_spot=1,
        car_id= 1,
    )

    # Attempt to book the same slot again
    slot_id_2 = get_slot_id(session, reservation_date_1)

    # Ensure the same slot cannot be booked again
    assert slot_id_2 is not None
    assert slot_id_1 == slot_id_2 + 1 

    slot2 = SlotModel.get_by_id(session, slot_id_2)
    assert slot2.start_time.hour == 11
    assert slot2.end_time.hour == 12

    # Booking for 12:00 (earlier time)
    reservation_date_3 = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
    slot_id_3 = get_slot_id(session, reservation_date_3)
    assert slot_id_3 is not None

    # Check if the returned slot ID corresponds to the 11:00-12:00 period
    reserved_slot_2 = SlotModel.get_by_id(session, slot_id_3)
    assert reserved_slot_2.start_time.hour == 11
    assert reserved_slot_2.end_time.hour == 12


def test_slot_unavailable(session, setup_database):
    create_hourly_slots(session)

    reservation_time = datetime.now().replace(hour=9, minute=30, second=0, microsecond=0)

    slot_id_1 = get_slot_id(session, reservation_time)

    reservation_1 = ReservationModel.add_reservation(
        session=session,
        slot_id=slot_id_1,
        service_id=1,
        customer_id=1,
        carwash_id = 1,
        reservation_date= reservation_time,
        parking_spot=1,
        car_id = 1,
    )

    assert SlotModel.get_by_id(session, slot_id_1).start_time.hour == 8

    with pytest.raises(Exception, match="Slot is not available for reservation"):
        reservation_1 = ReservationModel.add_reservation(
        session=session,
        slot_id=slot_id_1,
        service_id=1,
        customer_id=1,
        carwash_id = 1,
        reservation_date= reservation_time,
        parking_spot=1,
        car_id = 1,
    )
        
    reservation_time2 = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)

    slot_id_2  = get_slot_id(session, reservation_time2)
        
    reservation_2 = ReservationModel.add_reservation(
        session=session,
        slot_id=slot_id_1,
        service_id=1,
        customer_id=1,
        carwash_id = 1,
        reservation_date= reservation_time2,
        parking_spot=1,
        car_id = 1,
    )
    assert SlotModel.get_by_id(session, slot_id_1).start_time.hour == 8
    

def test_get_earliest_available_slot(session):
    create_hourly_slots(session)
    car = CarModel.add_car(session= session, license_plate = 'xx', car_type= 'small_car', car_brand = 'mazda')
    reservation_date_1 = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0) + timedelta(days=1)

    reservation_date_2 = datetime.now().replace(hour=11, minute=0, second=0, microsecond=0) + timedelta(days=1)
    reservation = ReservationModel.add_reservation(
        session=session,
        slot_id=1,
        service_id=1,
        customer_id=1,
        carwash_id=1,
        reservation_date=reservation_date_1,
        car_id=car.id,
        parking_spot=1,
    ) 
    time = get_earliest_available_slot(db_session = session,
                                reservation_date=reservation_date_2
                                )
    end_time  = SlotModel.get_by_id(session, 2).end_time + timedelta(days=1)

    assert time == end_time

def test_no_available_slots(session):
    # Create slots and make all of them reserved
    car = CarModel.add_car(session= session, license_plate = 'xx', car_type= 'small_car', car_brand = 'mazda')
    create_hourly_slots(session)
    
    # Reserve all slots
    for slot in SlotModel.get_all(session):
        ReservationModel.add_reservation(
            session=session,
            slot_id=slot.id,
            service_id=1,
            customer_id=1,
            carwash_id=1,
            reservation_date=slot.start_time,
            car_id=car.id,
            parking_spot=1,
        )

    reservation_date = datetime.now().replace(hour=9,minute=0, second=0, microsecond=0) + timedelta(hours=1)
    earliest_available_slot_end_time = get_earliest_available_slot(session, reservation_date)

    assert earliest_available_slot_end_time is None
