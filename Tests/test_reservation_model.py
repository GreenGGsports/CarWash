import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.models.reservation_model import ReservationModel
from src.models.extra_model import ExtraModel
from src.models.service_model import ServiceModel
from src.models.company_model import CompanyModel
from src.models.carwash_model import CarWashModel
from src.models.car_model import CarModel

@pytest.fixture
def setup_database(session: Session):
    # Clean up the database before the test starts
    session.query(ReservationModel).delete()
    session.query(ExtraModel).delete()
    session.query(ServiceModel).delete()
    session.query(CompanyModel).delete()
    session.commit()

    # Adding companies
    company1 = CompanyModel(company_name='Company 1', discount=10)
    session.add(company1)
    session.commit()

    # Adding car washes
    carwash1 = CarWashModel(carwash_name='Car Wash 1', location='Budapest')
    session.add(carwash1)
    session.commit()

    car1 = CarModel(license_plate='xyz-123', car_type = 'small_car', car_brand = 'Bugatti',company_id = company1.id )
    session.add(car1)
    session.commit()

    # Adding services
    service1 = ServiceModel(service_name='Service 1', price_small=50, price_large=80, carwash_id=carwash1.id)
    session.add(service1)
    session.commit()

    # Adding extras
    extra1 = ExtraModel(service_name='Extra 1', price=10, extra_type='interior', carwash_id=carwash1.id)
    extra2 = ExtraModel(service_name='Extra 2', price=15, extra_type='exterior', carwash_id=carwash1.id)
    session.add_all([extra1, extra2])
    session.commit()

    yield

    # Clean up the database after the test ends
    session.query(ReservationModel).delete()
    session.query(ExtraModel).delete()
    session.query(ServiceModel).delete()
    session.query(CompanyModel).delete()
    session.commit()

def test_add_reservation_nocompany(session: Session, setup_database):
    appointment = datetime.utcnow()

    # company1 = CompanyModel(company_name='Company 1', discount=10)
    # session.add(company1)

    # car = CarModel(license_plate='xyz-123', car_type = 'small_car', car_brand = 'Bugatti',company_id = company1.id )
    # session.add(car)
    # session.commit()

    # from pdb import set_trace
    # set_trace()
    from pdb import set_trace 
    set_trace()
    reservation = ReservationModel.add_reservation(
        session=session,
        slot_id=1,
        service_id=1,
        customer_id=1,
        carwash_id = 1,
        reservation_date= appointment,
        parking_spot=1,
        car_id = 1,
        extras=[],
    )
    
    assert reservation.id is not None

def test_add_reservation(session: Session, setup_database):
    appointment = datetime.utcnow()
    reservation = ReservationModel.add_reservation(
        session=session,
        slot_id=1,
        service_id=1,
        company_id=1,
        customer_id=1,
        carwash_id=1,
        reservation_date=appointment,
        parking_spot='A1',
        car_type='large_car',
        car_brand='Mazda',
        license_plate='ABC-123'
    )
    
    assert reservation.id is not None
    assert reservation.car_type == 'large_car'
    assert reservation.car_brand == 'Mazda'
    assert reservation.license_plate == 'ABC-123'
    assert reservation.final_price is not None

def test_read_reservation(session: Session, setup_database):
    reservation_date = datetime.utcnow()
    reservation = ReservationModel.add_reservation(
        session=session,
        slot_id=1,
        service_id=1,
        company_id=1,
        customer_id=1,
        carwash_id=1,
        reservation_date=reservation_date,
        parking_spot='B2',
        car_type='large_car',
        car_brand='Mazda',
        license_plate='ABC-123'
    )
    
    read_reservation = ReservationModel.get_by_id(session, reservation.id)
    assert read_reservation.id == reservation.id
    assert read_reservation.car_type == 'large_car'
    assert read_reservation.car_brand == 'Mazda'
    assert read_reservation.license_plate == 'ABC-123'

def test_update_reservation(session: Session, setup_database):
    appointment = datetime.utcnow()
    reservation = ReservationModel.add_reservation(
        session=session,
        slot_id=1,
        service_id=1,
        company_id=1,
        customer_id=1,
        carwash_id=1,
        reservation_date=appointment,
        parking_spot='C3',
        car_type='small_car',
        car_brand='Mazda',
        license_plate='ABC-123'
    )
    
    updated_reservation = ReservationModel.update_by_id(
        session=session,
        obj_id=reservation.id,
        car_type='large_car'
    )
    
    assert updated_reservation.car_type == 'large_car'

def test_delete_reservation(session: Session, setup_database):
    appointment = datetime.utcnow()
    reservation = ReservationModel.add_reservation(
        session=session,
        slot_id=1,
        service_id=1,
        company_id=1,
        customer_id=1,
        carwash_id=1,
        reservation_date=appointment,
        parking_spot='D4',
        car_type='large_car',
        car_brand='Mazda',
        license_plate='ABC-123'
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
    customer_id = 1
    carwash_id = 1
    reservation_date = datetime.utcnow() + timedelta(days=1)
    car_type = 'large_car'
    parking_spot = 1

    # Add an initial reservation
    ReservationModel.add_reservation(
        session=session,
        company_id=company_id,
        service_id=service_id,
        slot_id=slot_id,
        carwash_id=carwash_id,
        reservation_date=reservation_date,
        customer_id=customer_id,
        car_type=car_type,
        parking_spot=parking_spot,
        car_brand='Mazda',
        license_plate='ABC-123'
    )

    # Attempt to add a second reservation for the same slot and date
    with pytest.raises(Exception, match="Slot is not available for reservation"):
        ReservationModel.add_reservation(
            session=session,
            company_id=company_id,
            service_id=service_id,
            slot_id=slot_id,
            carwash_id=carwash_id,
            reservation_date=reservation_date,
            customer_id=customer_id,
            car_type=car_type,
            parking_spot=parking_spot,
            car_brand='Mazda',
            license_plate='DEF-456'
        )

        assert not ReservationModel.is_slot_available(session, slot_id, reservation_date)

def test_is_slot_available(session):
    # Sample data
    slot_id = 1
    reservation_date = datetime.now() + timedelta(days=1)

    try:
        # Ensure slot is available initially
        assert ReservationModel.is_slot_available(session, slot_id, reservation_date)

        # Add a reservation
        ReservationModel.add_reservation(
            session=session,
            company_id=1,
            service_id=1,
            slot_id=slot_id,
            carwash_id=1,
            reservation_date=reservation_date,
            customer_id=1,
            car_type='large_car',
            parking_spot=1,
            car_brand='Mazda',
            license_plate='ABC-123'
        )

        # Ensure slot is not available after reservation
        assert not ReservationModel.is_slot_available(session, slot_id, reservation_date)

    except Exception as e:
        session.rollback()  # Rollback changes if any exception occurs
        raise e

def test_add_multiple_extras(session):
    # Create ExtraModel objects and add them to the session
    extras = [
        ExtraModel(service_name='Extra 1', price=10, extra_type='interior', carwash_id=1),
        ExtraModel(service_name='Extra 2', price=15, extra_type='exterior', carwash_id=1),
        ExtraModel(service_name='Extra 4', price=20, extra_type='interior', carwash_id=1)
    ]
    session.add_all(extras)
    session.commit()

    # Now get the IDs of the added extras
    extra_ids = [extra.id for extra in extras]

    appointment = datetime.utcnow()

    # Add a reservation with the extra IDs
    reservation = ReservationModel.add_reservation(
        session=session,
        slot_id=1,
        service_id=1,
        customer_id=1,
        carwash_id = 1,
        reservation_date= appointment,
        parking_spot=1,
        car_id = 1,
        extras = extra_ids,
    )

    assert reservation is not None

    # Refresh the session to ensure the reservation is up-to-date
    session.refresh(reservation)

    # Assert that the extras are correctly associated with the reservation
    assert len(reservation.extras) == len(extra_ids)
    for extra_id in extra_ids:
        assert any(res_extra.id == extra_id for res_extra in reservation.extras)

    # Clean up
    session.close()

def test_correct_final_price_with_extras(session: Session, setup_database):
    appointment = datetime.utcnow() + timedelta(days=1)
    car_type = 'large_car'
    extras = [1, 2]  # Provide the IDs of the extra objects

    # Add a reservation
    reservation = ReservationModel.add_reservation(
        session=session,
        company_id=1,
        service_id=1,
        slot_id=1,
        carwash_id=1,
        reservation_date=appointment,
        customer_id=1,
        car_type=car_type,
        parking_spot='A1',
        extras=extras,
        car_brand='Mazda',
        license_plate='ABC-123'
    )

    assert reservation is not None

    # Fetch the service
    service = ServiceModel.get_by_id(session, reservation.service_id)
    assert service is not None

    # Fetch the company
    company = CompanyModel.get_by_id(session, reservation.company_id)
    assert company is not None

    # Fetch the extras
    reservation_extras = session.query(ExtraModel).filter(ExtraModel.id.in_(extras)).all()
    assert len(reservation_extras) == len(extras)

    service_price = 80
    extra1_price = 10
    extra2_price = 15
    discount = 10

    assert reservation.final_price == (service_price + extra1_price + extra2_price) * (1 - discount / 100)
