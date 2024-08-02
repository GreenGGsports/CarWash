from flask import current_app, Blueprint, request, session, jsonify
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, time
from src.models.slot_model import SlotModel
from src.models.reservation_model import ReservationModel

booking_ctrl = Blueprint('booking_ctrl', __name__, url_prefix='/booking')

@booking_ctrl.route('/set_date', methods= ["GET",'POST'])
def set_date():
    data = request.json
    date = datetime.strptime(data.get('date'),'%Y-%m-%d')
    session['reservation_date'] = date
    
    db_session = current_app.session_factory.get_session() 
    min_date = get_earliest_available_slot(
        db_session= db_session,
        reservation_date=date
    )
    if not min_date:
        return jsonify({'message': 'No slot available for reservation at this date.'})
    
    return jsonify({'min_date': min_date})

@booking_ctrl.route('/select_slot', methods=['POST'])
def select_slot():
    data = request.json
    reservation_date = data.get('date')
    if not reservation_date:
        return jsonify({'error': 'Date not provided'}), 400

    db_session = current_app.session_factory.get_session() 
    try:
        reservation_datetime = datetime.strptime(reservation_date, '%Y. %m. %d. %H:%M:%S')
        slot_id = get_slot_id(
            db_session= db_session,
            reservation_date=reservation_datetime
        )
        session['slot_id'] = slot_id
        session['reservation_date'] = reservation_datetime
        from pdb import set_trace
        set_trace()
        return jsonify({'message': 'Slot reserved successfully', 'reservation_date': reservation_datetime.isoformat()}), 200

    except ValueError:
        from pdb import set_trace
        set_trace()
        # Handle the case where the date format is incorrect
        return jsonify({'error': 'Invalid date format. Expected format is YYYY. MM. DD. HH:MM:SS'}), 400

    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': str(e)}), 500

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
            if datetime.combine(reservation_date.date(), time(hour=0, minute=0)) + timedelta(hours=slot.end_time.hour, minutes=slot.end_time.minute) < reservation_date:
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
    earliest_date = datetime.combine(reservation_date.date(), time(hour=0, minute=0)) + timedelta(hours=earliest_slot.end_time.hour, minutes=earliest_slot.end_time.minute)
    return earliest_date
