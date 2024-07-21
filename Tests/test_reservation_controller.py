import pytest
from flask import Flask, session
from datetime import datetime

from src.controllers.reservation_controller import reservation_ctrl  # Adjust import based on your project structure
from src.models.reservation_model import ReservationModel
from src.models.billing_model import BillingModel
from src.models.customer_model import CustomerModel

BLUEPRINT_ROUTE = '/reservation'
SHOW_FORM = '/'
ADD_RESERVATION = '/add'
SET_DATE = '/set_date'
ADD_BILLING = '/add_billing'

def test_show_reservation_form(client):
    response = client.get(BLUEPRINT_ROUTE + SHOW_FORM)
    assert response.status_code == 200
    assert b'Reservation Form Content' in response.data  # Adjust based on actual content of your form

def test_create_reservation_success(client, session):
    # Arrange
    with client.session_transaction() as sess:
        sess['slot_id'] = 1
        sess['service_id'] = 1
        sess['reservation_date'] = '2024-07-21'

    data = {
        'auto_tipus': 'kis_auto',
        'rendszam': 'ABC123',
        'parkolo': 'P1',
        'marka': 'Toyota',
        'parking_spot': 'P1',
        'vezeteknev2': 'Doe',
        'keresztnev2': 'John',
        'telefon': '123456789'
    }

    response = client.post(BLUEPRINT_ROUTE + ADD_RESERVATION, json=data)
    assert response.status_code == 200
    assert response.json['status'] == 'success'

    # Verify the reservation was added
    reservation = session.query(ReservationModel).first()
    assert reservation is not None
    assert reservation.license_plate == 'ABC123'
    assert reservation.car_brand == 'Toyota'

def test_create_reservation_failure(client, session):
    # Arrange
    with client.session_transaction() as sess:
        sess['slot_id'] = 1
        sess['service_id'] = 1
        sess['reservation_date'] = '2024-07-21'

    # Simulate a failure in adding reservation
    def failing_add_reservation(*args, **kwargs):
        raise AttributeError('Test error')

    with patch('src.controllers.reservation_controller.ReservationModel.add_reservation', side_effect=failing_add_reservation):
        data = {
            'auto_tipus': 'kis_auto',
            'rendszam': 'ABC123',
            'parkolo': 'P1',
            'marka': 'Toyota',
            'parking_spot': 'P1',
            'vezeteknev2': 'Doe',
            'keresztnev2': 'John',
            'telefon': '123456789'
        }

        response = client.post(BLUEPRINT_ROUTE + ADD_RESERVATION, json=data)
        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert 'Test error' in response.json['message']

def test_set_date(client):
    # Arrange
    data = {'date': '2024-07-21'}

    response = client.post(BLUEPRINT_ROUTE + SET_DATE, json=data)
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert sess['reservation_date'] == '2024-07-21'

def test_create_billing_success(client, session):
    # Arrange
    with client.session_transaction() as sess:
        sess['billing_id'] = None

    data = {
        'vezeteknev': 'Doe',
        'keresztnev': 'John',
        'cim': '123 Street',
        'email': 'john.doe@example.com',
        'cegnev': 'Doe Inc.',
        'adoszam': '123456789'
    }

    response = client.post(BLUEPRINT_ROUTE + ADD_BILLING, json=data)
    assert response.status_code == 200
    assert response.json['status'] == 'success'

    # Verify the billing data was added
    billing = session.query(BillingModel).first()
    assert billing is not None
    assert billing.email == 'john.doe@example.com'

def test_create_billing_failure(client, session):
    # Arrange
    def failing_add_billing_data(*args, **kwargs):
        raise AttributeError('Test error')

    with patch('src.controllers.reservation_controller.BillingModel.add_billing_data', side_effect=failing_add_billing_data):
        data = {
            'vezeteknev': 'Doe',
            'keresztnev': 'John',
            'cim': '123 Street',
            'email': 'john.doe@example.com',
            'cegnev': 'Doe Inc.',
            'adoszam': '123456789'
        }

        response = client.post(BLUEPRINT_ROUTE + ADD_BILLING, json=data)
        assert response.status_code == 400
        assert response.json['status'] == 'error'
        assert 'Test error' in response.json['message']
