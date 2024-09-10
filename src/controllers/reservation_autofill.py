from flask import Blueprint, request, jsonify, current_app, render_template, session
from flask_login import current_user
from src.models.customer_model import CustomerModel
from src.models.reservation_model import ReservationModel
from src.models.car_model import CarModel
from src.models.billing_model import BillingModel
from sqlalchemy.exc import SQLAlchemyError

reservation_autofill_ctrl = Blueprint('reservation_autofill_ctrl', __name__, url_prefix='/reservation_autofill')

@reservation_autofill_ctrl.route("/get_data")
def autofill():   
    if not current_user.is_authenticated:
        return jsonify({"error": "User not authenticated"}), 401

    session = current_app.session_factory.get_session()
    try:
        user_id = current_user.id
        customer = session.query(CustomerModel).filter(CustomerModel.user_id == user_id).order_by(CustomerModel.id.desc()).first()
        
        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        last_reservation = session.query(ReservationModel).filter(ReservationModel.customer_id == customer.id).order_by(ReservationModel.id.desc()).first()
        
        if not last_reservation:
            return jsonify({"error": "Last reservation not found"}), 404

        car = CarModel.get_by_id(session=session, obj_id=last_reservation.car_id)
        
        if not car:
            return jsonify({"error": "Car not found"}), 404

        billing = session.query(BillingModel).filter(BillingModel.reservation_id == last_reservation.id).order_by(BillingModel.id.desc()).first()

        data = dict(
            car_brand=car.car_brand,
            license_plate=car.license_plate,
            car_type='kis_auto' if car.car_type == 'small_car' else 'nagy_auto' if car.car_type == 'large_car' else None,
            telefon=customer.phone_number,
            parking_spot=last_reservation.parking_spot,
            vezeteknev2=customer.lastname,
            keresztnev2=customer.forname,
        )
        
        if billing:
            vezeteknev, keresztnev = billing.name.split(' ', 1) if ' ' in billing.name else (billing.name, '')
            billing_data = dict(
                vezeteknev=vezeteknev,
                keresztnev=keresztnev,
                cegnev=billing.company_name if billing.company_name else '',
                adoszam=billing.tax_ID if billing.tax_ID else '',
                email=billing.email if billing.email else '',
                cim=billing.address if billing.address else ''
            )
        else: 
            billing_data = False
        
        return jsonify({"reservation": data, "billing": billing_data})

    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error: {e}")
        return jsonify({"error": "A database error occurred"}), 500

    except Exception as e:
        current_app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

    finally:
        session.close()

