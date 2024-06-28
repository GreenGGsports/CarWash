from flask import Blueprint, request, jsonify, current_app
from src.models.billing_model import BillingModel

billing_ctrl = Blueprint('billing_ctrl', __name__, url_prefix='/reservation')

@billing_ctrl.route('/get_billing_data', methods=['GET', 'POST'])
def get_billing_data():
    data = request.json if request.method == 'POST' else request.args
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    license_plate = data.get('license_plate')
    if not license_plate:
        return jsonify({"error": "License plate not provided"}), 400
    
    session = current_app.session_factory.get_session()
    try:
        result_dict = BillingModel.get_first_by_license_plate(license_plate).__dict__
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
    
    return jsonify(result_dict if result_dict else {})