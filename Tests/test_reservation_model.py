# tests/test_reservation_model.py

import pytest
from app import db
from src.models.reservation_model import ReservationModel
from src.models.company_model import CompanyModel
from src.models.service_model import ServiceModel
import datetime

@pytest.fixture(scope='module')
def session():
    """Fixture to create a new SQLAlchemy session for each test function."""
    session = db.session
    yield session
    session.rollback()

def test_create_reservation(session):
    # Foglalás létrehozása
    reservation = ReservationModel(
        appointment=datetime.datetime.utcnow(),
        license_plate='ABC123',
        name='John Doe',
        phone_number='123456789',
        brand='Test Brand',
        type='Test Type',
        company_id=1,  # Itt az előre létrehozott Company id-jét használjuk
        service_id=1,  # Itt az előre létrehozott Service id-jét használjuk
        parking_spot='A1'
    )
    session.add(reservation)
    session.commit()

    # Ellenőrizzük, hogy a foglalás objektum létrejött-e
    assert reservation.id is not None

def test_read_reservation(session):
    # Foglalás kiolvasása az azonosító alapján
    reservation_id = 1  # Feltételezzük, hogy van egy ilyen ID-jű foglalás az adatbázisban
    reservation = session.query(ReservationModel).get(reservation_id)

    # Ellenőrizzük, hogy a megfelelő foglalás objektumot kaptuk-e vissza
    assert reservation is not None
    assert reservation.id == reservation_id

def test_update_reservation(session):
    # Foglalás frissítése az azonosító alapján
    reservation_id = 1  # Feltételezzük, hogy van egy ilyen ID-jű foglalás az adatbázisban
    updated_data = {
        'name': 'Updated Name',
        'phone_number': '999999999'
    }
    reservation = session.query(ReservationModel).get(reservation_id)
    for key, value in updated_data.items():
        setattr(reservation, key, value)
    session.commit()

    # Ellenőrizzük, hogy a frissített foglalás adatai megfelelőek-e
    updated_reservation = session.query(ReservationModel).get(reservation_id)
    assert updated_reservation.name == 'Updated Name'
    assert updated_reservation.phone_number == '999999999'

def test_delete_reservation(session):
    # Foglalás törlése az azonosító alapján
    reservation_id = 1  # Feltételezzük, hogy van egy ilyen ID-jű foglalás az adatbázisban
    reservation = session.query(ReservationModel).get(reservation_id)
    session.delete(reservation)
    session.commit()

    # Ellenőrizzük, hogy a törlés után a foglalás tényleg nem található-e az adatbázisban
    deleted_reservation = session.query(ReservationModel).get(reservation_id)
    assert deleted_reservation is None
