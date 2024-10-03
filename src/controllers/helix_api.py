from flask import Blueprint, jsonify, current_app
from sqlalchemy.orm import joinedload
from src.models.reservation_model import ReservationModel
from src.models.car_model import CarModel
from src.models.service_model import ServiceModel
from src.models.customer_model import CustomerModel
from src.models.carwash_model import CarWashModel

# Create the helix Blueprint
helix_api = Blueprint('helix_api', __name__,url_prefix='/helix')

@helix_api.route('/reservations', methods=['GET'])
def get_reservations():
    # Fetch reservation data with relationships
    session = current_app.session_factory.get_session()
    reservations = session.query(
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
     .join(CustomerModel, ReservationModel.customer_id == CustomerModel.id) \
     .all()

    # Serialize the data to JSON format
    results = []
    for res in reservations:
        results.append({
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
        

    return jsonify(results), 200
