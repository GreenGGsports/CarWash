from flask import Blueprint, jsonify, current_app, request
from sqlalchemy.orm import joinedload
from src.models.reservation_model import ReservationModel
from src.models.car_model import CarModel
from src.models.service_model import ServiceModel
from src.models.customer_model import CustomerModel
from src.models.carwash_model import CarWashModel

helix_api = Blueprint('helix_api', __name__)

@helix_api.route('/reservations', methods=['GET'])
def get_reservations():
    current_app.logger.debug('GET /reservations - Incoming request')

    # Extract query parameters
    license_plate = request.args.get('license_plate')
    reservation_id = request.args.get('id')

    current_app.logger.debug(f"Query params: license_plate={license_plate}, reservation_id={reservation_id}")

    session = current_app.session_factory.get_session()

    try:
        # Base query to fetch reservation data
        query = session.query(ReservationModel).options(
            joinedload(ReservationModel.car),  # Eager load related CarModel
            joinedload(ReservationModel.service),  # Eager load related ServiceModel
            joinedload(ReservationModel.customer),  # Eager load related CustomerModel
            joinedload(ReservationModel.carwash)  # Eager load related CarWashModel
        )

        # Apply filters based on query parameters
        if license_plate:
            current_app.logger.debug(f"Filtering by license_plate: {license_plate}")
            query = query.join(ReservationModel.car).filter(CarModel.license_plate == license_plate)
        if reservation_id:
            current_app.logger.debug(f"Filtering by reservation_id: {reservation_id}")
            query = query.filter(ReservationModel.id == reservation_id)

        reservations = query.all()
        current_app.logger.info(f"Found {len(reservations)} reservations")

        # Serialize the data
        items = []
        for res in reservations:
            items.append({
                'carwash_name': res.carwash.carwash_name,
                'reservation_date': res.reservation_date.strftime('%Y-%m-%d %H:%M:%S'),
                'license_plate': res.car.license_plate,
                'car_brand': res.car.car_brand,
                'car_model': res.car.car_model,
                'service_name': res.service.service_name,
                'phone_number': res.customer.phone_number,
                'final_price': res.final_price,
                'is_completed': res.is_completed
            })

        current_app.logger.debug("Successfully serialized reservation data")

        response = {
            "items": items
        }
        return jsonify(response), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching reservations: {str(e)}")
        return jsonify({'error': 'Failed to fetch reservations'}), 500

    finally:
        # Ensure session cleanup
        session.close()
