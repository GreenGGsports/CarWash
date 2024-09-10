from src.models.billing_model import BillingModel
from flask import Blueprint, current_app, jsonify, request ,session
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
import logging
billing_ctrl = Blueprint('billing_ctrl', __name__, url_prefix='/billing')

@billing_ctrl.route('/get_billing_data', methods=['GET'])
def get_billing_data():
    try:
        # Obtain a database session
        session = current_app.session_factory.get_session()
        
        if current_user.is_authenticated:
            user_id = current_user.id
            
            data = BillingModel.get_last_by_user_id(session=session, user_id=user_id)
            data_dict = data.__dict__ if data else {}
            return jsonify(data_dict)
        else:
            return jsonify({'error': 'User not authenticated'}), 401

    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error: {e}")
        return jsonify({'error': 'A database error occurred'}), 500

    except Exception as e:
        current_app.logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@billing_ctrl.route('/add_billing', methods=['POST'])   
def create_billing():
    data = request.json
    db_session = current_app.session_factory.get_session()
    data = parse_billing_data(data)
    try:
        reservation_id = session.get('reservation_id')
        billing_data = BillingModel.add_billing_data(db_session, reservation_id = reservation_id,**data)
        session['billing_id'] = billing_data.id
        return jsonify({'status': 'success'})
    except AttributeError as e:
        db_session.rollback()
        current_app.logger.error(f"AttributeError in create_billing: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 400

    except SQLAlchemyError as e:
        db_session.rollback()
        current_app.logger.error(f"Database error in create_billing: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to add billing data.'}), 500

    except Exception as e:
        db_session.rollback()
        current_app.logger.error(f"Unexpected error in create_billing: {e}")
        return jsonify({'status': 'error', 'message': 'An unexpected error occurred.'}), 500

def parse_billing_data(data):
    return dict(
        name = data.get('vezeteknev') + ' ' + data.get('keresztnev'),
        address = data.get('cim'),
        email = data.get('email'),
        company_name = data.get('cegnev'),
        tax_ID = data.get('adoszam')
    )