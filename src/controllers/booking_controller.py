from flask import current_app, Blueprint, request, session, jsonify
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, time
from src.models.slot_model import SlotModel
from src.models.reservation_model import ReservationModel
from sqlalchemy.exc import SQLAlchemyError
booking_ctrl = Blueprint('booking_ctrl', __name__, url_prefix='/booking')

@booking_ctrl.route('/set_date', methods=["GET", "POST"])
def set_date():
    response = {'status': 'error', 'message': 'An unexpected error occurred.'}
    if not request.json or 'date' not in request.json:
        response['message'] = 'Invalid or missing date parameter.'
        return jsonify(response), 400

    try:
        date_str = request.json.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError as ve:
        current_app.logger.error(f"Date parsing error: {ve}")
        response['message'] = 'Date format must be YYYY-MM-DD.'
        return jsonify(response), 400

    session['reservation_date'] = date
    
    try:
        db_session = current_app.session_factory.get_session()
        min_date = get_earliest_available_slot(
            db_session=db_session,
            reservation_date=date
        )
        if min_date is None:
            response['message'] = 'No slot available for reservation at this date.'
            return jsonify(response), 404

        response = {'status': 'success', 'min_date': min_date}
        return jsonify(response)

    except SQLAlchemyError as sqle:
        current_app.logger.error(f"Database error: {sqle}")
        response['message'] = 'Database error occurred while checking slot availability.'
        return jsonify(response), 500

    except Exception as e:
        current_app.logger.error(f"Unexpected error: {e}")
        return jsonify(response), 500

@booking_ctrl.route('/select_slot', methods=['POST'])
def select_slot():
    data = request.json
    if not data or 'date' not in data:
        current_app.logger.error("Date not provided in request.")
        return jsonify({'error': 'Date not provided'}), 400

    reservation_date_str = data.get('date')
    try:
        reservation_datetime = datetime.fromisoformat(reservation_date_str.replace('Z', ''))
    except ValueError as ve:
        current_app.logger.error(f"Date parsing error: {ve}")
        return jsonify({'error': 'Invalid date format. Expected format is YYYY. MM. DD. HH:MM:SS'}), 400

    db_session = current_app.session_factory.get_session()
    
    try:
        slot_id = get_slot_id(
            db_session=db_session,
            reservation_date=reservation_datetime
        )
        
        if slot_id is None:
            current_app.logger.warning(f"No slot available for the date: {reservation_datetime}")
            return jsonify({'error': 'No slot available for the provided date.'}), 404
        session['slot_id'] = slot_id
        session['reservation_date'] = reservation_datetime
        
        return jsonify({'message': 'Slot reserved successfully', 'reservation_date': reservation_datetime.isoformat()}), 200

    except SQLAlchemyError as sqle:
        current_app.logger.error(f"Database error: {sqle}")
        return jsonify({'error': 'Database error occurred while reserving slot.'}), 500

    except Exception as e:
        current_app.logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500

def get_available_slots(db_session: Session, date: datetime) -> list:
    try:
        live_slots = SlotModel.get_live_slots(db_session)

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

def get_slot_id(db_session: Session, reservation_date: datetime) -> int:
    try:
        available_slots = get_available_slots(
            db_session=db_session,
            date=reservation_date
        )
        
        if not available_slots:
            raise Exception("No available slots found.")

        latest_slot = None
        for slot in available_slots:
            slot_end_datetime = datetime.combine(reservation_date.date(), time(hour=0, minute=0)) + timedelta(hours=slot.end_time.hour, minutes=slot.end_time.minute)
            
            if slot_end_datetime <= reservation_date:
                if latest_slot is None or slot.start_time > latest_slot.start_time:
                    latest_slot = slot

        if latest_slot:
            return latest_slot.id
        else:
            raise Exception("No available slot before the given date.")

    except Exception as e:
        current_app.logger.error(f"Error finding slot ID: {e}")
        raise

def get_earliest_available_slot(db_session: Session, reservation_date: datetime) -> datetime:
    try:
        available_slots = get_available_slots(
            db_session=db_session,
            date=reservation_date
        )
        
        if not available_slots:
            current_app.logger.info("No available slots found for the reservation date.")
            return None

        earliest_slot = None
        for slot in available_slots:
            if earliest_slot is None or slot.start_time < earliest_slot.start_time:
                earliest_slot = slot

        if earliest_slot:
            earliest_date = datetime.combine(reservation_date.date(), time(hour=0, minute=0)) + timedelta(
                hours=earliest_slot.end_time.hour, minutes=earliest_slot.end_time.minute
            )
            current_app.logger.info(f"Earliest available slot found: {earliest_date}")
            return earliest_date
        else:
            current_app.logger.info("No earliest slot found before the reservation date.")
            return None

    except Exception as e:
        current_app.logger.error(f"Error finding the earliest available slot: {e}")
        raise
