from flask import current_app, Blueprint, request, session, jsonify
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, time
from src.models.slot_model import SlotModel
from src.models.carwash_model import CarWashModel
from src.models.reservation_model import ReservationModel
from sqlalchemy.exc import SQLAlchemyError
from src.models.slot_lock_model import SlotLockModel
from flask_login import current_user

booking_ctrl = Blueprint('booking_ctrl', __name__, url_prefix='/booking')

def get_available_slots(db_session: Session, date: datetime, carwash_id: int) -> list:
    try:
        # Lekérjük az aktív slotokat az adott carwash-hoz
        live_slots = db_session.query(SlotModel).filter_by(live=True, carwash_id=carwash_id).all()

        available_slots = []
        for slot in live_slots:
            # Ellenőrizzük, hogy a slot az adott napon szabad-e
            existing_lock = db_session.query(SlotLockModel).filter(
                SlotLockModel.slot_id == slot.id,
                SlotLockModel.reservation_date == date,
                SlotLockModel.locked_until > datetime.now()  # Még érvényben lévő zárolás
            ).first()

            if existing_lock:
                # Ha a slot zárolva van, ellenőrizzük, hogy az aktuális useré-e
                if existing_lock.user_id == current_user.id:
                    available_slots.append(slot)
            else:
                # Ellenőrizzük a tényleges foglaltságot
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
        date = datetime.strptime(data['date'], '%Y-%m-%d')
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
    
    available_slots = get_available_slots(db_session, date, carwash_id)
    response = []
    for slot in available_slots :
        if date >= slot.end_time:
            response.append(
                dict(
                    id = slot.id,
                    end_time_hours = slot.end_time.strftime('%H'),
                    end_time_minutes = slot.end_time.strftime('%M'),
                    available = True
                )
                )
    return jsonify({'success': True, 'slots': response})

@booking_ctrl.route('/api/carwash/reserve_slot', methods=['POST'])
def reserve_slot():
    try:
        db_session = current_app.session_factory.get_session()
        data = request.get_json()
        slot_id = data['slot_id']
        reservation_date = datetime.strptime(data['date'], '%Y-%m-%d').date()

        # A zárolás lejárati idejének beállítása (10 perc)
        lock_expiration = datetime.now() + timedelta(minutes=10)

        # Töröljük a korábbi zárolásokat ehhez a felhasználóhoz
        db_session.query(SlotLockModel).filter_by(user_id=current_user.id).delete()

        # Ellenőrizzük, hogy a slot már zárolva van-e más által
        existing_slot_lock = db_session.query(SlotLockModel).filter(
            SlotLockModel.slot_id == slot_id,
            SlotLockModel.reservation_date == reservation_date,
            SlotLockModel.locked_until > datetime.now()  # Zárolás érvényben van
        ).first()

        if existing_slot_lock:
            return jsonify({'success': False, 'message': 'A slot már tartalékban van másik felhasználó által.'})

        # Hozzuk létre az új zárolást
        new_lock = SlotLockModel(
            slot_id=slot_id,
            user_id=current_user.id,
            reservation_date=reservation_date,
            locked_until=lock_expiration
        )
        db_session.add(new_lock)
        db_session.commit()

        return jsonify({'success': True, 'message': 'Az időpont tartalékban van, 10 percig foglalva.'})

    except SQLAlchemyError as e:
        db_session.rollback()
        current_app.logger.error(f"Error reserving slot: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})