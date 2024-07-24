from flask import current_app, Blueprint
from sqlalchemy.orm import Session
from datetime import datetime
from src.models.slot_model import SlotModel
from src.models.reservation_model import ReservationModel

booking_ctrl = Blueprint('booking_ctrl', __name__, url_prefix='/booking')
def get_available_slots(db_session: Session, date: datetime) -> list:
    live_slots = SlotModel.get_live_slots(db_session)
    available_slots = []
    for slot in live_slots:
        if date >= slot.end_time:
            if ReservationModel.is_slot_available(
                session= db_session,
                slot_id=slot.id,
                reservation_date=date):
                available_slots.append(slot)
    return available_slots

def get_slot_id(db_session: Session, reservation_date: datetime) -> int:
    available_slots = get_available_slots(
        db_session=db_session,
        date= reservation_date
    )
                
    # Find the latest slot before the reservation_date
    latest_slot = None
    for slot in available_slots:
        if not latest_slot or slot.start_time >= latest_slot.start_time:
            latest_slot = slot
    
    if latest_slot:
        return latest_slot.id
    else:
        raise Exception("No available slot before the given date")

def get_earliest_available_slot(db_session: Session, reservation_date: datetime) -> datetime:
    available_slots = get_available_slots(
        db_session=db_session,
        date= reservation_date
    )
    if not available_slots:
        return None
    
    earliest_slot = None
    for slot in available_slots:
        if not earliest_slot or slot.start_time <= earliest_slot.start_time:
            earliest_slot = slot
    return earliest_slot.end_time
