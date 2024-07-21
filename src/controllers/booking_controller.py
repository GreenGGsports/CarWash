from sqlalchemy.orm import Session
from datetime import datetime
from src.models.slot_model import SlotModel
from src.models.reservation_model import ReservationModel

def get_slot_id(session: Session, reservation_date: datetime) -> int:
    available_slots = []
    live_slots = SlotModel.get_live_slots(session)
    
    for slot in live_slots:
        if reservation_date >= slot.end_time:
            if ReservationModel.is_slot_available(session, slot.id, reservation_date):
                available_slots.append(slot)
                
    # Find the latest slot before the reservation_date
    latest_slot = None
    for slot in available_slots:
        if not latest_slot or slot.start_time >= latest_slot.start_time:
            latest_slot = slot
    
    if latest_slot:
        return latest_slot.id
    else:
        raise Exception("No available slot before the given date")
    