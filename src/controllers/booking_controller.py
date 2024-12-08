from flask import current_app, Blueprint, request, session, jsonify
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, time
from src.models.slot_model import SlotModel
from src.models.carwash_model import CarWashModel
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
        carwash_id = session['carwash_id']
    except KeyError:
        response['message'] = 'Carwash ID not found in session.'
        return jsonify(response), 400

    
    try:
        db_session = current_app.session_factory.get_session()
        carwash = CarWashModel.get_by_id(db_session, carwash_id)
        is_open = carwash.is_open(db_session,date)
        
        min_date = get_earliest_available_slot(
            db_session=db_session,
            reservation_date=date,
            carwash_id = carwash_id
        )
        if min_date is None or is_open == False:
            response['message'] = 'No slot available for reservation at this date.'
            response['min_date'] = datetime.combine(date, time.max) - timedelta(hours=2)
            return jsonify(response)

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
        current_app.logger.error("Date or carwash_id not provided in request.")
        return jsonify({'error': 'Date or carwash_id not provided'}), 400

    reservation_date_str = data.get('date')
    carwash_id = session.get('carwash_id')

    if carwash_id is None:
        current_app.logger.error("Carwash ID not found in session.")
        return jsonify({'error': 'Carwash ID not found in session'}), 400
    
    try:
        reservation_datetime = datetime.fromisoformat(reservation_date_str.replace('Z', ''))
    except ValueError as ve:
        current_app.logger.error(f"Date parsing error: {ve}")
        return jsonify({'error': 'Invalid date format. Expected format is YYYY. MM. DD. HH:MM:SS'}), 400

    db_session = current_app.session_factory.get_session()
    
    try:
        slot_id = get_slot_id(
            db_session=db_session,
            reservation_date=reservation_datetime,
            carwash_id=carwash_id
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


def get_slot_id(db_session: Session, reservation_date: datetime, carwash_id: int) -> int:
    try:
        available_slots = get_available_slots(
            db_session=db_session,
            date=reservation_date,
            carwash_id=carwash_id
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

def get_earliest_available_slot(db_session: Session, reservation_date: datetime, carwash_id: int) -> datetime:
    try:
        available_slots = get_available_slots(
            db_session=db_session,
            date=reservation_date,
            carwash_id=carwash_id
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