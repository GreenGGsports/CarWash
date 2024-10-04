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
    # Log that the reservations endpoint has been hit
    current_app.logger.info('GET /reservations - Incoming request')

    # Extract query parameters
    license_plate = request.args.get('license_plate')
    reservation_id = request.args.get('id')
    
    current_app.logger.info(f"Query params: license_plate={license_plate}, reservation_id={reservation_id}")

    # Get session from session factory
    session = current_app.session_factory.get_session()

    # Base query to fetch reservation data
    query = session.query(
        CarWashModel.carwash_name,
        ReservationModel.reservation_date,
        CarModel.license_plate,
        CarModel.car_brand,
        CarModel.car_model,
        ServiceModel.service_name,
        ReservationModel.extras,
        CustomerModel.phone_number,
        ReservationModel.payment_method,
        ReservationModel.final_price,
        ReservationModel.is_completed
    ).join(CarWashModel, ReservationModel.carwash_id == CarWashModel.id) \
     .join(CarModel, ReservationModel.car_id == CarModel.id) \
     .join(ServiceModel, ReservationModel.service_id == ServiceModel.id) \
     .join(CustomerModel, ReservationModel.customer_id == CustomerModel.id)

    # Apply filters based on query parameters
    if license_plate:
        current_app.logger.info(f"Filtering by license_plate: {license_plate}")
        query = query.filter(CarModel.license_plate == license_plate)
    if reservation_id:
        current_app.logger.info(f"Filtering by reservation_id: {reservation_id}")
        query = query.filter(ReservationModel.id == reservation_id)

    try:
        # Fetch filtered reservations
        reservations = query.all()
        current_app.logger.info(f"Found {len(reservations)} reservations")
        
        # Serialize the data to JSON format
        items = []
        for res in reservations:
            items.append({
                'carwash_name': res[0],
                'reservation_date': res[1].strftime('%Y-%m-%d %H:%M:%S'),
                'license_plate': res[2],
                'car_brand': res[3],
                'car_model': res[4],
                'service_name': res[5],
                'extras': res[6],  # Adjust if extras is a relationship or JSON
                'phone_number': res[7],
                'final_price': res[9],
                'is_completed': res[10]
            })
        
        current_app.logger.info("Successfully serialized reservation data")

        # Build the response in the desired format
        response = {
            "items": items
        }

        return jsonify(response), 200
    
    except Exception as e:
        current_app.logger.error(f"Error fetching reservations: {str(e)}")
        return jsonify({'error': 'Failed to fetch reservations'}), 500
