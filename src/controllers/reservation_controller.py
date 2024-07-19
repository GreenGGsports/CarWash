from flask import Blueprint, request, jsonify,current_app,render_template, session
from src.models.reservation_model import ReservationModel
from  datetime import datetime
from flask_login import current_user
from src.models.billing_model import BillingModel
from src.models.customer_model import CustomerModel

reservation_ctrl = Blueprint('reservation_ctrl', __name__, url_prefix='/reservation')

@reservation_ctrl.route('/')
def show_reservation_form():
    return render_template('reservation.html')

@reservation_ctrl.route('/add', methods=['POST'])
def create_reservation():
    db_session = current_app.session_factory.get_session()
    data = request.json
    data = {key: value for key, value in data.items() if value != ''}
    car_type, license_plate, parking_spot, car_brand, parking_spot = parse_reservation_data(data)
    customer_id = add_customer(data)
    slot_id, service_id, extra_ids, carwash_id, billing_id, researvation_date = get_session_data()
    ReservationModel.add_reservation(
        session=db_session,
        slot_id= 2,
        service_id=service_id,
        customer_id=customer_id,
        carwash_id=carwash_id,
        billing_id=billing_id,
        reservation_date=researvation_date,
        parking_spot=parking_spot,
        license_plate = license_plate,
        car_brand= car_brand, 
        car_type = car_type,
    )
    return jsonify({'status': 'success'})

def get_session_data():
    slot_id = session.get('slot_id')
    service_id = session.get('service_id')
    extra_ids = session.get('extra_ids')
    #not implemented
    carwash_id = session.get('carwash_id')
    billing_id = session.get('billing_id') 
    researvation_date = datetime.strptime(session.get('reservation_date'), '%Y-%m-%d')
    return slot_id, service_id, extra_ids, carwash_id, billing_id, researvation_date 

@reservation_ctrl.route('/set_date', methods= ['POST'])
def set_date():
    data = request.json
    date = data.get('date')
    session['reservation_date'] = date
    return {}

@reservation_ctrl.route('/add_billing',methods=['POST'])
def create_billing():
    data = request.json
    db_session = current_app.session_factory.get_session()
    data = parse_billing_data(data)
    billing_data = BillingModel.add_billing_data(
        db_session, **data)
    session['billing_id'] = billing_data.id
    return {}

def parse_reservation_data(data):
    if  data.get('auto_tipus') == 'kis_auto':
        car_type = 'small_car'
    elif data.get('auto_tipus') == 'nagy_auto':
        car_type = 'large_car'
        
    license_plate = data.get('rendszam')
    parking_spot = data.get('parkolo')
    car_brand = data.get('marka')
    parking_spot = data.get('parking_spot')
    return car_type, license_plate, parking_spot, car_brand, parking_spot

def parse_customer_data(data):
    return dict(
        forname = data.get('vezeteknev2'),
        lastname = data.get('keresztnev2'),
        phone_number = data.get('telefon'),
        
    )
def add_customer(data):
    db_session = current_app.session_factory.get_session()
    customer_data = parse_customer_data(data)
    user_id = session.get('user_id')
    if user_id and CustomerModel.get_lat_by_user_id(session=db_session,user_id=user_id):
        customer = CustomerModel.update_by_id(session=db_session,**customer_data)
        return customer.id
    else: 
        customer = CustomerModel.add_customer(db_session,**customer_data)
        return customer.id
        
        
        
def parse_billing_data(data):
    return dict(
        name = data.get('vezeteknev') + ' ' + data.get('keresztnev'),
        address = data.get('cim'),
        email = data.get('email'),
        company_name = data.get('cegnev'),
        tax_ID = data.get('adoszam'), 
        user_id = session.get('user_id')
    )

        
        
        

