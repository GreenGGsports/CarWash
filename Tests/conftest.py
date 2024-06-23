# tests/conftest.py

import pytest
from setup import create_app
from src.models.reservation_model import ReservationModel
from src.models.company_model import CompanyModel
from src.models.service_model import ServiceModel
import datetime

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')
    testing_client = flask_app.test_client()

    with flask_app.app_context():
        db.create_all()

        company = CompanyModel(company_name='Test Company')
        service = ServiceModel(service_name='Test Service')
        db.session.add(company)
        db.session.add(service)
        db.session.commit()

        reservation = ReservationModel(
            appointment=datetime.datetime.utcnow(),
            license_plate='ABC123',
            name='John Doe',
            phone_number='123456789',
            brand='Test Brand',
            type='Test Type',
            company_id=company.id,
            service_id=service.id,
            parking_spot='A1'
        )
        db.session.add(reservation)
        db.session.commit()

    yield testing_client

    with flask_app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def init_database():
    flask_app = create_app('testing')
    with flask_app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()