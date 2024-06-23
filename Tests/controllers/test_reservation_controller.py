import unittest
from unittest.mock import patch, MagicMock
from src.models.reservation_model import ReservationModel
from datetime import datetime
from setup import create_app

class ReservationControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')  # Create your Flask app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        # Create an application context
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create a request context
        self.request_context = self.app.test_request_context()
        self.request_context.push()

    def tearDown(self):
        # Pop contexts
        self.request_context.pop()
        self.app_context.pop()

    @patch('src.controllers.reservation_controller.current_app')
    @patch('src.controllers.reservation_controller.request')
    def test_create_reservation_success(self, mock_request, mock_current_app):

        mock_session = MagicMock()
        mock_current_app.session_factory.get_session.return_value = mock_session
        data = {
            'appointment': '2023-07-10T15:30',
            'license_plate': 'ABC123',
            'name': 'John Doe',
            'phone_number': '1234567890',
            'brand': 'Toyota',
            'type': 'SUV',
            'company_id': 1,
            'service_id': 2,
            'parking_spot': 5
        }
        
        mock_request.json = data

        mock_reservation = MagicMock()
        mock_reservation.id = 1
        mock_reservation.appointment = datetime.strptime(data['appointment'], '%Y-%m-%dT%H:%M')
        mock_reservation.name = data['name']
        mock_reservation.service_id = data['service_id']

        ReservationModel.add_reservation = MagicMock(return_value=mock_reservation)
        response = self.client.post('/reservation/add')
        response_data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data['message'], 'Reservation added successfully!')
        self.assertEqual(response_data['reservation']['id'], 1)
        self.assertEqual(response_data['reservation']['name'], data['name'])
        self.assertEqual(response_data['reservation']['service_id'], data['service_id'])

    @patch('src.controllers.reservation_controller.current_app')
    @patch('src.controllers.reservation_controller.request')
    def test_create_reservation_failure(self, mock_request, mock_current_app):
        mock_session = MagicMock()
        mock_current_app.session_factory.get_session.return_value = mock_session
        
        data = {
            'appointment': 'invalid date',
            'license_plate': 'ABC123',
            'name': 'John Doe',
            'phone_number': '1234567890',
            'brand': 'Toyota',
            'type': 'SUV',
            'company_id': 1,
            'service_id': 2,
            'parking_spot': 5
        }
        
        mock_request.json = data

        response = self.client.post('/reservation/add')
        response_data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response_data)
        self.assertIn('Incorrect data format', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
