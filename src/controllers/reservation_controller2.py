from flask import current_app 
from src.models.service_model import ServiceModel
from src.models.carwash_model import CarWashModel
from src.models.extra_model import ExtraModel
from src.models.customer_model import CustomerModel
from src.models.slot_model import SlotModel
from src.models.car_model import CarModel, CarTypeEnum
from src.models.reservation_model import ReservationModel
from src.models.billing_model import BillingModel
from flask_login import current_user
    
def create_reservation(session, carwash, service, extras, slot, car, customer, reservation_data, admin=False):
    try:
        reservation = ReservationModel(
            car_id=car.id,
            service_id=service.id,
            slot_id=slot.id,
            carwash_id=carwash.id,
            customer_id=customer.id,
            extras=extras,
            **reservation_data.kwargs
        )
        
        if admin and reservation_data.final_price:
            reservation.final_price = reservation_data.final_price
        else:
            reservation.calculate_final_price(session=session)
        
        session.add(reservation)
        session.commit()
        return reservation
    except Exception as e:
        current_app.logger.error(f"Failed to create reservation: {e}", exc_info=True)
        session.rollback()
        raise

def create_billing(session, reservation, billing_data):
    try:
        billing = BillingModel(
            reservation_id=reservation.id,
            **billing_data.kwargs
        )
        session.add(billing)
        session.commit()
    except Exception as e:
        current_app.logger.error(f"Failed to create billing: {e}", exc_info=True)
        session.rollback()
        raise


def add_car(session, car_data):
    try:
        license_plate = car_data.kwargs.get('license_plate')
        if not license_plate:
            raise ValueError("License plate is required to add or update a car.")
        
        car = session.query(CarModel).filter_by(license_plate=license_plate).first()
        if car:
            current_app.logger.info(f"Updating existing car with license plate: {license_plate}")
            car.car_type = car_data.kwargs.get('car_type', car.car_type)
            car.car_brand = car_data.kwargs.get('car_brand', car.car_brand)
            car.car_model = car_data.kwargs.get('car_model', car.car_model)
        else:
            current_app.logger.info(f"Adding new car with license plate: {license_plate}")
            car = CarModel(**car_data.kwargs)
        
        session.add(car)
        session.commit()
        return car
    except ValueError as ve:
        current_app.logger.error(f"Validation error: {ve}")
        session.rollback()
        raise
    except Exception as e:
        current_app.logger.error(f"Failed to add or update car: {e}", exc_info=True)
        session.rollback()
        raise


def add_customer(session, customer_data, admin=False):
    try:
        customer = create_customer(session, customer_data, admin)
        session.add(customer)
        session.commit()
        return customer
    except Exception as e:
        current_app.logger.error(f"Failed to add customer: {e}", exc_info=True)
        session.rollback()
        raise

def create_customer(session, customer_data, admin=False):
    try:
        if admin:
            return CustomerModel(**customer_data.kwargs)

        if not admin and not current_user.is_authenticated:
            current_app.logger.warning("Unauthenticated user attempting to create a customer.")
            return CustomerModel(**customer_data.kwargs)

        existing_customer = session.query(CustomerModel).filter_by(user_id=current_user.id).first()

        if not existing_customer:
            customer = CustomerModel(**customer_data.kwargs)
            customer.user_id = current_user.id
            return customer

        current_app.logger.info(f"Updating existing customer for user_id: {current_user.id}")
        existing_customer.forname = customer_data.kwargs.get('forname', existing_customer.forname)
        existing_customer.lastname = customer_data.kwargs.get('lastname', existing_customer.lastname)
        existing_customer.phone_number = customer_data.kwargs.get('phone_number', existing_customer.phone_number)
        return existing_customer
    except Exception as e:
        current_app.logger.error(f"Failed to create or update customer: {e}", exc_info=True)
        raise
        
    
        
    
