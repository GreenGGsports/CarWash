from src.models.billing_model import BillingModel
from flask import Blueprint, current_app, jsonify, request
from flask_login import current_user

billing_ctrl = Blueprint('billing_ctrl', __name__, url_prefix='/billing')

billing_ctrl.route('/get_billing_data', methods=['GET'])    
def get_billing_data():
    session = current_app.session_factory.get_session()
    if current_user.is_authenticated:
        user_id = current_user.id
        data = BillingModel.get_last_by_user_id(session=session, user_id=user_id).__dict__
        return jsonify(data) if data else jsonify({})
    else:
        return jsonify({})

billing_ctrl.route('/save_billing_data', methods=['POST'])    
def save():
    data = request.json
    session = current_app.session_factory.get_session()
    
    kwargs = parse_response(data)
    BillingModel.add_billing_data(
        session=session, 
        **kwargs
                                  )
    

def parse_response(data):
    license_plate = data.get('license_plate')
    name = data.get('name')
    address = data.get('address')
    email = data.get('email')
    company_name = data.get('company_name')
    tax_ID =  data.get('tax_id')
    user_id = current_user.id
    reservation_id = current_user.reservation_id
    
    return dict(
        license_plate = license_plate,
        name = name,
        address = address,
        email = email,
        company_name = company_name,
        tax_ID = tax_ID,
        user_id = user_id,
        reserervation_id = reservation_id 
    )