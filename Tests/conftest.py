# tests/conftest.py

import pytest
from app import create_app, db
from src.models.reservation_model import ReservationModel
from src.models.company_model import CompanyModel
from src.models.service_model import ServiceModel
import datetime

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')  # 'testing' konfiguráció használata
    testing_client = flask_app.test_client()

    # Adatbázis inicializálása a tesztekhez
    with flask_app.app_context():
        db.create_all()

        # Példa adatok létrehozása a CompanyModel és ServiceModel alapján
        company = CompanyModel(company_name='Test Company') 
        service = ServiceModel(service_name='Test Service')
        db.session.add(company)
        db.session.add(service)
        db.session.commit()

        # Példa adatok létrehozása a ReservationModel alapján
        reservation = ReservationModel(
            appointment=datetime.datetime.utcnow(),
            license_plate='ABC123',
            name='John Doe',
            phone_number='123456789',
            brand='Test Brand',
            type='Test Type',
            company=company,
            service=service,
            parking_spot='A1'
        )
        db.session.add(reservation)
        db.session.commit()

    yield testing_client  # Teszteknek visszaadjuk a teszt klienst

    # Tesztek utáni takarítás
    with flask_app.app_context():
        db.session.remove()
        db.drop_all()
