from flask import Blueprint, request, jsonify,current_app,render_template, session
from src.models.reservation_model import ReservationModel
import datetime
from flask_login import current_user
from src.models.billing_model import BillingModel

reservation_ctrl = Blueprint('reservation_ctrl', __name__, url_prefix='/reservation')

@reservation_ctrl.route('/')
def show_reservation_form():
    return render_template('reservation.html')

@reservation_ctrl.route('/add', methods=['POST'])
def create_reservation():
    data = request.json
    data = {key: value for key, value in data.items() if value != ''}
    reservation_data = parse_reservation_data(data)
    from pdb import set_trace
    set_trace()
    return jsonify({'status': 'success'})

@reservation_ctrl.route('/set_date', methods= ['POST'])
def set_date():
    data = request.json
    date = data.get('date')

@reservation_ctrl.route('/add_billing',methods=['POST'])
def create_billing():
    data = request.json
    return {}

def parse_reservation_data(data):
    if  data.get('auto_tipus') == 'kis_auto':
        car_type = 'small_car'
    elif data.get('auto_tipus') == 'nagy_auto':
        car_type = 'large_car'
    return dict(
        forname = data.get('vezeteknev2'),
        lastname = data.get('keresztnev2'),
        phone_number = data.get('telefon'),
        license_plate = data.get('rendszam'),
        parking_spot = data.get('parkolo'), 
        car_type = car_type,
        car_brand = data.get('marka'),
        
        
    )
def parse_billing_data(data):
    return dict(
        name = data.get('vezeteknev'),
        address = data.get('cím'),
        email = data.get('email'),
        company_name = data.get('cegnev'),
        tax_ID = data.get('')    
    )

        
        
        

