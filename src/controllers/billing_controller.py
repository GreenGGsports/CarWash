from src.models.billing_model import BillingModel
from flask import Blueprint, current_app, jsonify, request ,session
from flask_login import current_user

billing_ctrl = Blueprint('billing_ctrl', __name__, url_prefix='/billing')

@billing_ctrl.route('/get_billing_data', methods=['GET'])    
def get_billing_data():
    session = current_app.session_factory.get_session()
    if current_user.is_authenticated:
        user_id = current_user.id
        data = BillingModel.get_last_by_user_id(session=session, user_id=user_id).__dict__
        return jsonify(data) if data else jsonify({})
    else:
        return jsonify({})

@billing_ctrl.route('/add_billing', methods=['POST'])   
def create_billing():
    data = request.json
    db_session = current_app.session_factory.get_session()
    data = parse_billing_data(data)
    from pdb import set_trace
    set_trace()
    try:
        billing_data = BillingModel.add_billing_data(
            db_session, **data
            )
        session['billing_id'] = billing_data.id
        return jsonify({'status': 'success'})
    
    except AttributeError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'An unexpected error occurred.'}), 500
    

def parse_billing_data(data):
    return dict(
        name = data.get('vezeteknev') + ' ' + data.get('keresztnev'),
        address = data.get('cim'),
        email = data.get('email'),
        company_name = data.get('cegnev'),
        tax_ID = data.get('adoszam')
    )