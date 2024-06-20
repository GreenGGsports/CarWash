import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from setup import create_app

app = create_app('testing')

def test_create_reservation_success():
    with app.test_client() as client:
        # Mock JSON data for the reservation
        data = {
            'appointment': '2024-06-20T15:00:00',
            'license_plate': 'ABC123',
            'name': 'John Doe',
            'phone_number': '1234567890',
            'brand': 'Toyota',
            'type': 'Sedan',
            'company_id': 1,
            'service_id': 2,
            'parking_spot': 'A1'
        }
        
        # Send a POST request to the '/add' endpoint
        response = client.post('/add', json=data)
        
        # Assert the response status code
        assert response.status_code == 201
        
        # Assert the response JSON data
        data = json.loads(response.data.decode('utf-8'))
        assert 'message' in data
        assert data['message'] == 'Reservation added successfully!'
        assert 'reservation' in data
        reservation = data['reservation']
        assert 'id' in reservation
        assert 'appointment' in reservation
        assert 'name' in reservation
        assert 'service_id' in reservation
        # Add more assertions as per your response structure
