from flask import Blueprint, request, jsonify
from src.models.reservation_model import Reservation
from src.views.reservation_view import ReservationView

reservation_ctrl = Blueprint('reservation_ctrl', __name__, url_prefix='/reservation')

@reservation_ctrl.route('/')
def show_reservation_form():
    return ReservationView.show_reservation_form()

@reservation_ctrl.route('/add', methods=['POST'])
def create_reservation():
    data = request.json
    
    appointment = data.get('appointment')
    license_plate = data.get('license_plate')
    name = data.get('name')
    phone_number = data.get('phone_number')
    brand = data.get('brand')
    type = data.get('type')
    company_id = data.get('company_id')
    service_id = data.get('service_id')
    parking_spot = data.get('parking_spot')
    
    try:
        reservation = Reservation.add_reservation(
            appointment=appointment,
            license_plate=license_plate,
            name=name,
            phone_number=phone_number,
            brand=brand,
            type=type,
            company_id=company_id,
            service_id=service_id,
            parking_spot=parking_spot
        )

        return jsonify({'message': 'Reservation added successfully!', 'reservation': {
            'id': reservation.id,
            'appointment': reservation.appointment.isoformat(),
            'name': reservation.name,
            'service_id': reservation.service_id
        }}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400
