from flask import Blueprint, request, jsonify, current_app, render_template, session
from src.models.reservation_model import ReservationModel
from  datetime import datetime
from flask_login import current_user
from src.models.billing_model import BillingModel
from src.models.customer_model import CustomerModel
from src.models.service_model import ServiceModel
from src.models.carwash_model import CarWashModel
from src.models.extra_model import ExtraModel
from src.models.car_model import CarModel, CarTypeEnum
from src.views.reservation_view import ReservationView
from jinja2 import Template
reservation_ctrl = Blueprint('reservation_ctrl', __name__, url_prefix='/reservation')

@reservation_ctrl.route('/')
def show_reservation_form():
    return render_template('Foglalas.html')

@reservation_ctrl.route('/add', methods=['POST'])
def create_reservation():
    db_session = current_app.session_factory.get_session()
    data = request.json
    data = {key: value for key, value in data.items() if value != ''}
    car_type, license_plate, parking_spot, car_brand = parse_reservation_data(data)
    car_id = add_car(car_type, license_plate, car_brand)
    customer_id = add_customer(data)
    slot_id, service_id, extra_ids, carwash_id,  reservation_date = get_session_data()
    try:
        reservation = ReservationModel.add_reservation(
            session=db_session,
            slot_id=slot_id,
            service_id=service_id,
            customer_id=customer_id,
            carwash_id=carwash_id,
            reservation_date=reservation_date,
            parking_spot=parking_spot,
            car_id=car_id, 
            extras= extra_ids,
        )
        session['reservation_id'] = reservation.id
        current_app.logger.info(f"Reservation created successfully with ID {reservation.id}.")
        return jsonify({'status': 'success'}), 200
    
    except AttributeError as e:
        current_app.logger.error(f"AttributeError while creating reservation: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 400
    
    except ValueError as e:
        current_app.logger.error(f"ValueError while creating reservation: {e}")
        return jsonify({'status': 'error', 'message': 'Invalid data format.'}), 400
    
    except Exception as e:
        current_app.logger.error(f"Unexpected error while creating reservation: {e}")
        return jsonify({'status': 'error', 'message': 'An unexpected error occurred.'}), 500
    
def add_customer(data):
    db_session = current_app.session_factory.get_session()
    customer_data = parse_customer_data(data)

    try:
        if current_user.is_authenticated:
            user_id = int(current_user.id)
            # Check if the user already has a customer record
            existing_customer = CustomerModel.get_last_by_user_id(session=db_session, user_id=user_id)
            if existing_customer:
                customer = CustomerModel.update_by_id(session=db_session, **customer_data)
                current_app.logger.info(f"Customer record updated for user_id {user_id}.")
            else:
                customer = CustomerModel.add_customer(db_session,user_id=user_id, **customer_data)
                current_app.logger.info(f"New customer record added for user_id {user_id}.")
        else:
            customer = CustomerModel.add_customer(db_session, **customer_data)
            current_app.logger.info("New customer record added with no associated user_id.")
        
        db_session.commit()
        return customer.id
    
    except AttributeError as e:
        db_session.rollback()
        current_app.logger.error(f"AttributeError while adding/updating customer: {e}")
        raise
    
    except Exception as e:
        db_session.rollback()
        current_app.logger.error(f"Unexpected error while adding/updating customer: {e}")
        raise
    
def add_car(car_type, license_plate, car_brand):
    db_session = current_app.session_factory.get_session()
    try:
        # Check if the car with the same license plate already exists
        cars = CarModel.filter_by_column_value(
            session=db_session,
            column_name='license_plate',
            value=license_plate
        )
        
        if cars:
            car = cars[0]
            # Update the existing car record
            CarModel.update_by_id(
                session=db_session,
                obj_id=car.id,
                license_plate=license_plate,
                car_type=car_type,
                car_brand=car_brand
                # Add company_id if implemented
            )
            current_app.logger.info(f"Updated car record with license_plate {license_plate}.")
        else:
            # Add a new car record
            car = CarModel.add_car(
                session=db_session,
                license_plate=license_plate,
                car_type=car_type,
                car_brand=car_brand
                # Add company_id if implemented
            )
            current_app.logger.info(f"Added new car record with license_plate {license_plate}.")
        
        # Store the car ID in the session
        session['car_id'] = car.id
        return car.id

    except Exception as e:
        db_session.rollback()
        current_app.logger.error(f"An error occurred while adding/updating car: {e}")
        raise
    
    
def get_session_data():
    slot_id = session.get('slot_id')
    service_id = session.get('service_id')
    extra_ids = session.get('extra_ids')

    #not implemented
    carwash_id = session.get('carwash_id')
    researvation_date = session.get('reservation_date')
    return slot_id, service_id, extra_ids, carwash_id, researvation_date 


def parse_reservation_data(data):
    if  data.get("auto_meret") == 'kis_auto':
        car_type = 'small_car'
    elif data.get("auto_meret") == 'nagy_auto':
        car_type = 'large_car'
        
    license_plate = data.get('rendszam')
    parking_spot = data.get('parkolo')
    car_brand = data.get('marka')
    parking_spot = data.get('parking_spot')
    #not implemented
    car_model = data.get('model')
    return car_type, license_plate, parking_spot, car_brand

def parse_customer_data(data):
    return dict(
        forname = data.get('vezeteknev2'),
        lastname = data.get('keresztnev2'),
        phone_number = data.get('telefon'),
        
    )
            
def get_popup_data():
    try:
        slot_id, service_id, extra_ids, carwash_id, researvation_date = get_session_data()
        db_session = current_app.session_factory.get_session()
        reservation_id = session.get('reservation_id')
        
        car_id = session.get('car_id')
        car = CarModel.get_by_id(session=db_session, obj_id=car_id) 
        
        car_size = car.car_type
        license_plate = car.license_plate
        location = CarWashModel.get_value_by_id(session=db_session,obj_id = carwash_id, column_name='location')
        service_name = ServiceModel.get_value_by_id(session=db_session, obj_id=service_id, column_name= 'service_name')
        
        if car_size == CarTypeEnum.small_car:
            service_price = ServiceModel.get_value_by_id(session=db_session, obj_id=service_id, column_name= 'price_small')
        
        elif car_size == CarTypeEnum.large_car:
            service_price = ServiceModel.get_value_by_id(session=db_session, obj_id=service_id, column_name= 'price_small')
            
        final_price = ReservationModel.get_value_by_id(session=db_session, obj_id=reservation_id, column_name= 'final_price')
        researvation_date = session.get('reservation_date')
        
        extra_price = 0
        extra_names = ""
        if extra_ids:
            extra_price = 0
            extra_names = []
            for extra_id in extra_ids:
                extra = ExtraModel.get_by_id(session=db_session,obj_id= extra_id)
                extra_price += extra.price
                extra_names.append(extra.service_name)
    except Exception as e:
        current_app.logger.error(f"Error occurred while generating data for popup HTML: {e}")
    return location , license_plate, researvation_date, service_name, service_price, extra_names, extra_price, final_price


@reservation_ctrl.route('/popup')
def get_popup():
    try:
        location , license_plate, researvation_date, service_name, service_price, extra_names, extra_price, final_price = get_popup_data()
        # Render the template with replacements
        data = dict(
            hely=location,
            rendszam= license_plate,
            csomag=  service_name,
            service_price = service_price,
            extra = extra_names,
            extra_price = extra_price,
            idopont= researvation_date,
            vegosszeg= final_price,
        )
            
        return jsonify(data)
    except Exception as e:
        current_app.logger.error(f"Error occurred while generating popup HTML: {e}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500
        

