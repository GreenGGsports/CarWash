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
    
def create_reservation(carwash, service, extras, slot, reservation_data ,admin=False):
    session = current_app.session_factory.get_session()
    reservation = ReservationModel(
        car_id=1,
        service_id=service.id,
        slot_id=slot.id,
        carwash_id=carwash.id,
        customer_id =1,
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

def create_billing(reservation, billing_data):
    session = current_app.session_factory.get_session()
    billing = BillingModel(
        reservation_id=reservation.id,
        **billing_data.kwargs
    )
    session.add(billing)
    session.commit()
    return
