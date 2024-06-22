import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from flask import Flask
from src.controllers.reservation_controller import reservation_ctrl
from flask import Flask, current_app, json

@pytest.fixture
def app():
    """Create and configure a test app instance."""
    app = Flask(__name__)
    app.config['TESTING'] = True  # Set TESTING config to True
    app.register_blueprint(reservation_ctrl)
    yield app

@pytest.fixture
def client(app):
    """Create a test client using the Flask application."""
    return app.test_client()

def test_show_reservation_form(client):
    """Test the show_reservation_form endpoint."""
    with patch('src.controllers.reservation_controller.ReservationView.show_reservation_form') as mock_show_form:
        mock_show_form.return_value = 'Mocked form HTML'
        response = client.get('/reservation/')
        assert response.status_code == 200
        assert response.data.decode() == 'Mocked form HTML'
        mock_show_form.assert_called_once()
        


def test_create_reservation(client):
    """Test the create_reservation endpoint."""
    mock_session = MagicMock()
    mock_add_reservation = MagicMock()
    mock_session_factory = MagicMock()
    mock_session_factory.get_session.return_value = mock_session
    mock_reservation_model = MagicMock()
    mock_reservation_model.add_reservation.return_value = MagicMock(
        id=1,
        appointment=datetime(2024, 6, 25, 10, 0),
        name='John Doe',
        service_id=3
    )
    
    with patch.object(current_app, 'session_factory', mock_session_factory), \
         patch('src.models.reservation_model.ReservationModel', mock_reservation_model):
        
        json_data = {
            'appointment': '2024-06-25T10:00',
            'license_plate': 'ABC123',
            'name': 'John Doe',
            'phone_number': '1234567890',
            'brand': 'Toyota',
            'type': 'SUV',
            'company_id': 1,
            'service_id': 3,
            'parking_spot': 'A1'
        }
        
        # Use app.app_context() to manually activate application context
        with app.app_context():
            response = client.post('/reservation/add', json=json_data)
        
        assert response.status_code == 201
        assert mock_session_factory.get_session.called
        assert mock_reservation_model.add_reservation.called
        
        data = json.loads(response.data.decode())
        assert 'message' in data
        assert 'reservation' in data
        assert data['reservation']['id'] == 1
        assert data['reservation']['appointment'] == '2024-06-25T10:00:00'
        assert data['reservation']['name'] == 'John Doe'
        assert data['reservation']['service_id'] == 3