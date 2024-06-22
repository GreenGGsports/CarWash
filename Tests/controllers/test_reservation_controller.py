import pytest
from flask import Flask, jsonify
from src.controllers.reservation_controller import reservation_ctrl
from setup import create_app, db
from unittest.mock import patch, MagicMock
import datetime
from sqlalchemy.orm import sessionmaker
@pytest.fixture
def app():
    app = create_app('development')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_show_reservation_form(client):
    with patch('src.views.reservation_view.ReservationView.show_reservation_form') as mock_show_form:
        mock_show_form.return_value = "Reservation Form"
        
        response = client.get('/reservation/')
        
        mock_show_form.assert_called_once()
        assert response.status_code == 200
        assert response.data == b"Reservation Form"

@patch('src.models.reservation_model.ReservationModel.add_reservation')
def test_create_reservation(mock_add_reservation, client):
    date = datetime.datetime.now()
    mock_reservation = MagicMock()
    mock_reservation.id = 1
    mock_reservation.appointment =date
    mock_reservation.license_plate = "ABC123"
    mock_reservation.name = "John Doe"
    mock_reservation.phone_number = "1234567890"
    mock_reservation.brand = "Toyota"
    mock_reservation.type = "Sedan"
    mock_reservation.company_id = 1
    mock_reservation.service_id = 2
    mock_reservation.parking_spot = "A1"
    mock_add_reservation.return_value = mock_reservation
    
    data = {
        "appointment": date,
        "license_plate": "ABC123",
        "name": "John Doe",
        "phone_number": "1234567890",
        "brand": "Toyota",
        "type": "Sedan",
        "company_id": 1,
        "service_id": 2,
        "parking_spot": "A1"
    }
    
    response = client.post('/reservation/add', json=data)
    
    print(response.get_json())  # Print the response data for debugging
    from pdb import set_trace
    set_trace()
    mock_add_reservation.assert_called_once_with(
        appointment=date,
        license_plate="ABC123",
        name="John Doe",
        phone_number="1234567890",
        brand="Toyota",
        type="Sedan",
        company_id=1,
        service_id=2,
        parking_spot="A1"
    )
    assert response.status_code == 201
    response_json = response.get_json()
    assert response_json['message'] == 'Reservation added successfully!'
    assert response_json['reservation'] == {
        'id': 1,
        'appointment': "2024-06-21T10:00:00",
        'name': "John Doe",
        'service_id': 2
    }

def test_create_reservation_missing_data(client):
    data = {
        "appointment": "2024-06-21T10:00:00",
        "license_plate": "ABC123",
        "name": "John Doe",
        "phone_number": "1234567890",
        "brand": "Toyota",
        "type": "Sedan"
        # Missing company_id, service_id, and parking_spot
    }
    
    response = client.post('/reservation/add', json=data)
    
    assert response.status_code == 400
    response_json = response.get_json()
    assert 'error' in response_json
    print(response_json)  # Print the response data for debugging
    

