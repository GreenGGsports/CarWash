from flask import Blueprint, request, jsonify, current_app, render_template, session
from src.models.reservation_model import ReservationModel
from  datetime import datetime
from flask_login import current_user
from src.models.billing_model import BillingModel
from src.models.customer_model import CustomerModel
from src.models.car_model import CarModel
from src.views.reservation_view import ReservationView
reservation_ctrl = Blueprint('reservation_ctrl', __name__, url_prefix='/reservation')

@reservation_ctrl.route('/')
def show_reservation_form():
    return render_template('Foglalasi_rendszer.html')

def show_popup():
    return ReservationView.generate_popup_html(
        hely = 'BP', 
        elerhetosegek = '1111' ,
        rendszam = 'XD', 
        csomag = 'XD', 
        extra = 'fugázás', 
        idopont = 'p8', 
        vegosszeg = 100
    )

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
        return jsonify({'status': 'success'})
    except AttributeError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'An unexpected error occurred.'}), 500
    
def add_customer(data):
    db_session = current_app.session_factory.get_session()
    customer_data = parse_customer_data(data)
    user_id = session.get('user_id')

    try:
        if user_id and CustomerModel.get_last_by_user_id(session=db_session, user_id=user_id):
            customer = CustomerModel.update_by_id(session=db_session, **customer_data)
        else:
            customer = CustomerModel.add_customer(db_session, **customer_data)
        db_session.commit()
        return customer.id
    except AttributeError as e:
        db_session.rollback()
        print(f"AttributeError: {e}")
        raise
    except Exception as e:
        db_session.rollback()
        print(f"An error occurred: {e}")
        raise
    
def add_car(car_type, license_plate, car_brand):
    db_session = current_app.session_factory.get_session()
    
    try:
        cars = CarModel.filter_by_column_value(
            session=db_session,
            column_name='license_plate',
            value= license_plate
            )
        if cars:
            car = cars[0]
            car = CarModel.update_by_id(
                session =  db_session,
                obj_id = car.id,
                license_plate = license_plate,
                car_type = car_type,
                car_brand = car_brand,
                #not implemented
                #company_id = company_id 
                )
                
        else:
            car = CarModel.add_car(
                session= db_session,
                license_plate=license_plate,
                car_type=car_type,
                car_brand=car_brand
                #not implemented
                #company_id = company_id 
            )
        return car.id
    except Exception as e:
        db_session.rollback()
        print(f"An error occurred: {e}")
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
    if  data.get('auto_tipus') == 'kis_auto':
        car_type = 'small_car'
    elif data.get('auto_tipus') == 'nagy_auto':
        car_type = 'large_car'
        
    license_plate = data.get('rendszam')
    parking_spot = data.get('parkolo')
    car_brand = data.get('marka')
    parking_spot = data.get('parking_spot')
    return car_type, license_plate, parking_spot, car_brand

def parse_customer_data(data):
    return dict(
        forname = data.get('vezeteknev2'),
        lastname = data.get('keresztnev2'),
        phone_number = data.get('telefon'),
        
    )
        
        
        

