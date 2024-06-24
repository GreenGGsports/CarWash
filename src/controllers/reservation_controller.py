from flask import Blueprint, request, jsonify, current_app
from src.models.reservation_model import ReservationModel
from src.views.reservation_view import ReservationView
import datetime

reservation_ctrl = Blueprint('reservation_ctrl', __name__, url_prefix='/reservation')

@reservation_ctrl.route('/')
def show_reservation_form():
    return ReservationView.show_reservation_form()

@reservation_ctrl.route('/add', methods=['POST'])
def create_reservation():
    data = request.json
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    try:    
        appointment, license_plate, name, phone_number, brand, type, company_id, service_id, parking_spot  = parse_response(data)
    except KeyError as e:
        return jsonify({'error': f'Missing field {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': f"Incorrect data format: {str(e)}"}), 400
        
    session = current_app.session_factory.get_session()
    
    try:
        reservation = ReservationModel.add_reservation(
            session=session,
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
    
    finally:
        # Close the session to release resources
        session.close()
    
def parse_response(data):
    appointment = data.get('appointmentDate')
    appointment = datetime.datetime.strptime(appointment, '%Y-%m-%d')
    
    license_plate = data.get('license_plate')
    name = data.get('name')
    phone_number = data.get('phone_number')
    brand = data.get('brand')
    type = data.get('type')
    company_id = data.get('company_id')
    service_id = data.get('service_id')
    parking_spot = data.get('parking_spot')
    
    
    return appointment, license_plate, name, phone_number, brand, type, company_id, service_id, parking_spot 

