from flask import Blueprint, jsonify, request, current_app
from src.models.car_model import CarModel
from src.models.reservation_model import ReservationModel

car_ctrl = Blueprint('car_ctrl', __name__)

@car_ctrl.route('/get_car_data', methods=['GET'])
def autocomplete():
    license_plate = request.args.get('license_plate')
    if not license_plate:
        return jsonify({'error': 'License plate is required'}), 400

    # Lekérdezi az utolsó foglalást a rendszám alapján
    session = current_app.session_factory.get_session()
    reservation = (
        session.query(ReservationModel)
        .join(CarModel)
        .filter(CarModel.license_plate == license_plate)
        .order_by(ReservationModel.reservation_date.desc())
        .first()
    )

    if reservation:
        response = {
            'new_car_license_plate': reservation.car.license_plate,
            'new_car_type': reservation.car.car_type.name,
            'new_car_brand': reservation.car.car_brand,
            'customer_forname': reservation.customer.forname,
            'customer_lastname': reservation.customer.lastname,
            'customer_phone_number': reservation.customer.phone_number,
            'service': reservation.service.service_name,
            'reservation_date': reservation.reservation_date.strftime('%Y-%m-%d %H:%M:%S'),
            'parking_spot': reservation.parking_spot,
            'carwash': reservation.carwash.carwash_name,
        }
        return jsonify(response)
    else:
        return jsonify({'error': 'No reservation found'}), 404
