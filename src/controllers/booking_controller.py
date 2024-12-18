from flask import current_app, Blueprint, request, session, jsonify
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, time
from src.models.slot_model import SlotModel
from src.models.carwash_model import CarWashModel
from src.models.reservation_model import ReservationModel
from sqlalchemy.exc import SQLAlchemyError

booking_ctrl = Blueprint('booking_ctrl', __name__, url_prefix='/booking')

def get_available_slots(db_session: Session, date: datetime, carwash_id: int) -> list:
    try:
        live_slots = db_session.query(SlotModel).filter_by(live=True, carwash_id=carwash_id).all()

        available_slots = []
        for slot in live_slots:
            if date >= slot.end_time:
                if ReservationModel.is_slot_available(
                    session=db_session,
                    slot_id=slot.id,
                    reservation_date=date
                ):
                    available_slots.append(slot)

        return available_slots

    except Exception as e:
        current_app.logger.error(f"Error fetching available slots: {e}")
        raise
    
@booking_ctrl.route('/api/carwash/get_slots', methods=['POST'])
def get_carwash_slots():
    try:
        db_session = current_app.session_factory.get_session()
        data = request.get_json()
        date = datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
        carwash_id = int(data['carwash_id'])

        available_slots = get_available_slots(db_session, date, carwash_id)
        
        # Convert slot objects to a list of dictionaries for JSON response
        slots_data = [{'id': slot.id, 'start_time': slot.start_time.strftime('%H:%M'), 'end_time': slot.end_time.strftime('%H:%M')} for slot in available_slots]
        
        return jsonify({'success': True, 'slots': slots_data})

    except Exception as e:
        current_app.logger.error(f"Error fetching carwash slots: {e}")
        return jsonify({'success': False, 'error': str(e)})
    
@booking_ctrl.route('/api/carwash/get_slots2', methods=['POST'])
def get_slots():
    db_session = current_app.session_factory.get_session()
    data = request.get_json()
    date = datetime.strptime(data['date'], '%Y-%m-%d')
    carwash_id = session['carwash_id']
    
    live_slots = db_session.query(SlotModel).filter_by(live=True, carwash_id=carwash_id).all()
    response = []
    for slot in live_slots:
        if date >= slot.end_time:
            if ReservationModel.is_slot_available(
                session=db_session,
                slot_id=slot.id,
                reservation_date=date
            ):
                response.append(
                    dict(
                        id = slot.id,
                        end_time_hours = slot.end_time.strftime('%H'),
                        end_time_minutes = slot.end_time.strftime('%M'),
                        available = True
                    )
                )
            else:  
                response.append(
                    dict(
                        id = slot.id,
                        end_time_hours = slot.end_time.strftime('%H'),
                        end_time_minutes = slot.end_time.strftime('%M'),
                        available = False
                    )
                )
    return jsonify({'success': True, 'slots': response})